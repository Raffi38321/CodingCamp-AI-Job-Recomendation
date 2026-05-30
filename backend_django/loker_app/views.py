import os
import pickle
import numpy as np
import time
import json

from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, status
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers

# Menggunakan ONNX Runtime (Gudang komputasi ringan kita)
import onnxruntime as ort
# from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.metrics.pairwise import cosine_similarity

from .models import Loker
from .serializers import LokerSerializer

# ==========================================
# 1. VARIABEL GLOBAL UNTUK CACHING
# ==========================================
MAX_LEN = 299

ort_session = None
input_name_cv = None
input_name_job = None
output_name = None

tokenizer = None
tfidf_vectorizer = None

# Cache Data Job
GLOBAL_LOKER_DATA = []
GLOBAL_SEQ_JOB = None
GLOBAL_TFIDF_MATRIX_JOB = None

def manual_texts_to_sequences(texts, word_index, oov_token_id):
    """
    Pengganti fungsi texts_to_sequences milik Keras.
    Murni menggunakan Python, 0% Keras.
    """
    # Filter bawaan Keras yang dihapus saat tokenisasi
    filters = '!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n'
    translate_map = str.maketrans(filters, ' ' * len(filters))
    
    sequences = []
    for text in texts:
        # Ubah huruf kecil dan hilangkan tanda baca
        text = text.lower().translate(translate_map)
        seq = []
        for word in text.split():
            if word in word_index:
                seq.append(word_index[word])
            elif oov_token_id is not None:
                seq.append(oov_token_id)
        sequences.append(seq)
    return sequences

def manual_pad_sequences(sequences, maxlen, padding='post', value=0):
    hasil = np.full((len(sequences), maxlen), value, dtype=np.int32)
    
    for i, seq in enumerate(sequences):
        if len(seq) == 0:
            continue
            
        # Potong (truncate) jika panjang urutan melebihi batas maxlen
        if len(seq) > maxlen:
            seq = seq[:maxlen] # Potong bagian belakang
            
        # Masukkan angka ke dalam matriks sesuai jenis padding
        if padding == 'post':
            # Padding di belakang (angka diisi dari depan)
            hasil[i, :len(seq)] = seq
        else:
            # Padding di depan (angka diisi di belakang)
            hasil[i, -len(seq):] = seq
    return hasil

def init_system():
    global ort_session, input_name_cv, input_name_job, output_name
    global tokenizer, tfidf_vectorizer
    global GLOBAL_LOKER_DATA, GLOBAL_SEQ_JOB, GLOBAL_TFIDF_MATRIX_JOB
    global oov_token_id
    
    ONNX_PATH = os.path.join(settings.BASE_DIR, './../model_hasil/model_rekomendasi_3.onnx')
    TOKENIZER_PATH = os.path.join(settings.BASE_DIR, './../model_hasil/tokenizer_dict3.json')
    TFIDF_PATH = os.path.join(settings.BASE_DIR, './../model_hasil/tfidf_fitted.pkl')

    print("🚀 Memulai inisialisasi sistem ML (ONNX) dan Caching Database...")
    
    try:
        sess_options = ort.SessionOptions()
        sess_options.intra_op_num_threads = 1
        sess_options.inter_op_num_threads = 1
        
        
        # Load ONNX Session
        ort_session = ort.InferenceSession(str(ONNX_PATH), sess_options)
        
        # Ambil nama input secara otomatis dari model ONNX
        input_name_cv = ort_session.get_inputs()[0].name
        input_name_job = ort_session.get_inputs()[1].name
        output_name = ort_session.get_outputs()[0].name

        # Load Pickle
        with open(TOKENIZER_PATH, 'rb') as f:
            tokenizer_data = json.load(f)
        tokenizer = tokenizer_data['word_index']
        oov_token_id = tokenizer.get(tokenizer_data.get('oov_token'))
        
        with open(TFIDF_PATH, 'rb') as f:
            tfidf_vectorizer = pickle.load(f)

        semua_loker = list(Loker.objects.all())
        if not semua_loker:
            print("⚠️ Database loker kosong.")
            return

        GLOBAL_LOKER_DATA = semua_loker
        semua_teks_lowongan = []
        daftar_judul = []

        for loker in semua_loker:
            lokasi = f"{loker.kota or ''} {loker.provinsi or ''}".strip()
            teks_gabungan = f"{loker.industri or ''} {loker.kategori or ''} {loker.pendidikan or ''} {loker.tipe or ''} {lokasi} {loker.skills or ''} {loker.deskripsi or ''}".strip()
            
            semua_teks_lowongan.append(teks_gabungan)
            daftar_judul.append(loker.judul or "")

        # Pre-compute & pastikan formatnya np.float32 (Kewajiban ONNX)
        GLOBAL_SEQ_JOB = manual_pad_sequences(manual_texts_to_sequences(semua_teks_lowongan, tokenizer, oov_token_id), maxlen=MAX_LEN, padding='post').astype(np.float32)
        GLOBAL_TFIDF_MATRIX_JOB = tfidf_vectorizer.transform(daftar_judul)

        print(f"✅ Sistem ONNX siap! {len(GLOBAL_LOKER_DATA)} lowongan telah di-cache.")

    except Exception as e:
        print(f"❌ Gagal inisialisasi ONNX: {e}")

init_system()

# ==========================================
# 2. VIEW API
# ==========================================
class InferensiAPIView(APIView):
    
    @extend_schema(
        request=inline_serializer(
            name="RequestCV",
            fields={
                "title": serializers.CharField(),
                "industri": serializers.CharField(),
                "kategori": serializers.CharField(),
                "pendidikan": serializers.CharField(),
                "tipe": serializers.CharField(),
                "skills": serializers.CharField()
            }
        ),
        description="Menerima teks CV dan mengembalikan Top 30 rekomendasi dengan instan."
    )
    def post(self, request):
        waktu_mulai = time.time()
        
        if ort_session is None or tokenizer is None:
            return Response({"error": "Sistem ML belum siap."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        if not GLOBAL_LOKER_DATA:
            return Response({"error": "Database loker kosong"}, status=status.HTTP_404_NOT_FOUND)

        text_cv_title = request.data.get('title', '')
        text_cv_user = (
            request.data.get('industri', '') + " " +
            request.data.get('kategori', '') + " " +
            request.data.get('pendidikan', '') + " " +
            request.data.get('tipe', '') + " " +
            request.data.get('skills', '')
        )
        
        if not text_cv_title or not text_cv_user.strip():
            return Response({"error": "Semua field wajib diisi"}, status=status.HTTP_400_BAD_REQUEST)

        jumlah_lowongan = len(GLOBAL_LOKER_DATA)

        # 1. Proses CV User
        sequence_mentah_cv = manual_texts_to_sequences([text_cv_user], tokenizer, oov_token_id)
        seq_cv = manual_pad_sequences(sequence_mentah_cv, maxlen=MAX_LEN, padding='post').astype(np.float32)
        seq_cv_batch = np.repeat(seq_cv, jumlah_lowongan, axis=0)
        
        tfidf_cv = tfidf_vectorizer.transform([text_cv_title])

        BATCH_SIZE = 128  
        prediksi_onnx_list = []
        
        # Looping memotong data menjadi kelompok-kelompok kecil
        for i in range(0, jumlah_lowongan, BATCH_SIZE):
            batas_akhir = min(i + BATCH_SIZE, jumlah_lowongan)
            
            # Ambil potongan matriks sesuai ukuran batch
            batch_seq_job = GLOBAL_SEQ_JOB[i:batas_akhir]
            batch_seq_cv = seq_cv_batch[i:batas_akhir]
            
            ort_inputs_batch = {
                input_name_cv: batch_seq_cv,
                input_name_job: batch_seq_job
            }
            
            # Prediksi hanya untuk 128 data, lalu simpan hasilnya
            batch_pred = ort_session.run([output_name], ort_inputs_batch)[0].flatten()
            prediksi_onnx_list.extend(batch_pred)
        
        prediksi_onnx = np.array(prediksi_onnx_list)

        # 3. Prediksi TF-IDF
        skor_tfidf = cosine_similarity(tfidf_cv, GLOBAL_TFIDF_MATRIX_JOB).flatten()

        # 4. Kalkulasi & Sorting
        skor_gabungan = (prediksi_onnx * 0.5) + (skor_tfidf * 0.5)
        top_30_index = np.argsort(skor_gabungan)[::-1][:30]

        # 5. Susun Respons dari Memori
        hasil_rekomendasi = []
        for urutan, idx in enumerate(top_30_index):
            loker_obj = GLOBAL_LOKER_DATA[idx]
            hasil_rekomendasi.append({
                "ranking": urutan + 1,
                "skor_kecocokan": round(float(skor_gabungan[idx]), 4),
                "detail_loker": LokerSerializer(loker_obj).data
            })

        waktu_selesai = time.time()
        print(f"⚡ Waktu Inferensi ONNX Total: {waktu_selesai - waktu_mulai:.4f} detik")

        return Response({
            "pesan": "Inferensi ONNX berhasil",
            "total_lowongan_dianalisis": jumlah_lowongan,
            "waktu_proses_detik": round(waktu_selesai - waktu_mulai, 4),
            "rekomendasi": hasil_rekomendasi
        }, status=status.HTTP_200_OK)

class LokerViewSet(viewsets.ModelViewSet):
    queryset = Loker.objects.all()
    serializer_class = LokerSerializer