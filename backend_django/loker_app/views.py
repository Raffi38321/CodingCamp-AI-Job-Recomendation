import os
import pickle
import numpy as np
    
from django.shortcuts import render

from rest_framework import viewsets, status
from .models import Loker
from .serializers import LokerSerializer
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Embedding, Bidirectional, LSTM, GlobalAveragePooling1D, Concatenate, Dense, Dropout

from .models import Loker
from .serializers import LokerSerializer

# ==========================================
# 1. LOAD MODEL & TOKENIZER SECARA GLOBAL
# ==========================================
model = None
tokenizer = None

# 2. BUAT FUNGSI UNTUK MEMBANGUN ULANG ARSITEKTUR MODEL
def build_model():
    # ===================================================================
    # ⚠️ COPY-PASTE KODE ARSITEKTUR DARI COLAB KE SINI
    # Ini hanya contoh struktur, pastikan sama persis dengan yang di Colab!
    # ===================================================================
    input_cv = Input(shape=(MAX_LEN,), name='input_cv')
    input_job = Input(shape=(MAX_LEN,), name='input_job')
    
    # Shared Embedding
    shared_embedding = Embedding(input_dim=10000, output_dim=64, name='shared_embedding')
    
    cv_emb = shared_embedding(input_cv)
    job_emb = shared_embedding(input_job)
    
    # Proses LSTM / BiLSTM (Sesuaikan dengan arsitekturmu)
    shared_lstm = Bidirectional(LSTM(64, return_sequences=False))
    
    cv_vec = shared_lstm(cv_emb)
    job_vec = shared_lstm(job_emb)
    
    # Penggabungan
    concat = Concatenate()([cv_vec, job_vec])
    
    # Otak Klasifikasi
    x = Dense(64, activation='relu')(concat)
    output = Dense(1, activation='sigmoid')(x)
    
    # Bungkus menjadi Model
    model = Model(inputs=[input_cv, input_job], outputs=output)
    return model

# WEIGHTS_PATH = os.path.join(settings.BASE_DIR, './../model_hasil/model_loker.weights.h5')

MODEL_PATH = os.path.join(settings.BASE_DIR, './../model_hasil/model_rekomendasi_loker.keras')
TOKENIZER_PATH = os.path.join(settings.BASE_DIR, './../model_hasil/tokenizer_loker.pkl')

# Pastikan MAX_LEN ini sama persis dengan yang kamu gunakan saat di Colab!
MAX_LEN = 150

print("Sedang memuat ML Model dan Tokenizer ke dalam memori...")
try:
    # model = build_model()
    # model.load_weights(WEIGHTS_PATH)
    model = load_model(MODEL_PATH, compile=False) # compile=False karena kita hanya butuh untuk inferensi, bukan training
    with open(TOKENIZER_PATH, 'rb') as f:
        print("Memuat tokenizer...")
        tokenizer = pickle.load(f)
    print("Model berhasil dimuat!")
except Exception as e:
    print(f"Gagal memuat model: {e}")


class LokerViewSet(viewsets.ModelViewSet):
    # Mengambil semua data loker dari database
    queryset = Loker.objects.all()
    # Menggunakan serializer yang baru saja kita buat
    serializer_class = LokerSerializer

# Create your views here.
class InferensiAPIView(APIView):
    # Konfigurasi ini hanya untuk mempercantik tampilan di Swagger UI
    @extend_schema(
        request=inline_serializer(
            name="RequestCV",
            fields={"cv_text": serializers.CharField()}
        ),
        description="Menerima teks CV, mencocokkannya dengan semua loker, dan mengembalikan Top 20."
    )
    def post(self, request):
        if model is None :
            return Response(
                {"error": "Model ML gagal dimuat. Silakan cek terminal server Django untuk melihat error path file."}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        if tokenizer is None:
            return Response(
                {"error": "Tokenizer gagal dimuat. Pastikan file tokenizer_loker.pkl berada di path yang benar."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )    
            
        # 1. Ambil input CV dari user
        text_cv_user = request.data.get('cv_text')
        if not text_cv_user:
            return Response({"error": "Field 'cv_text' wajib diisi"}, status=status.HTTP_400_BAD_REQUEST)

        # 2. Ambil semua data loker dari database
        semua_loker = list(Loker.objects.all())
        if not semua_loker:
            return Response({"error": "Database loker masih kosong"}, status=status.HTTP_404_NOT_FOUND)

        # 3. Bentuk ulang "text_gabungan" untuk setiap loker seperti saat training di Colab
        semua_teks_lowongan = []
        for loker in semua_loker:
            # Sesuaikan atribut ini dengan kolom yang kamu pakai saat membuat text_gabungan di CSV
            judul = loker.judul or ""
            industri = loker.industri or ""
            kategori = loker.kategori or ""
            pendidikan = loker.pendidikan or ""
            tipe = loker.tipe or ""
            lokasi = f"{loker.kota or ''} {loker.provinsi or ''}".strip()
            skills = loker.skills or ""
            deskripsi = loker.deskripsi or ""
            
            teks_gabungan = f"{judul} {industri} {kategori} {pendidikan} {tipe} {lokasi} {skills} {deskripsi}".strip()
            semua_teks_lowongan.append(teks_gabungan) 

        # 4. Gandakan CV user
        jumlah_lowongan = len(semua_loker)
        teks_cv_digandakan = [text_cv_user] * jumlah_lowongan

        # 5. Tokenisasi & Padding
        seq_cv = pad_sequences(tokenizer.texts_to_sequences(teks_cv_digandakan), maxlen=MAX_LEN, padding='post')
        seq_job = pad_sequences(tokenizer.texts_to_sequences(semua_teks_lowongan), maxlen=MAX_LEN, padding='post')

        # 6. Prediksi (Mendapatkan probabilitas)
        skor_prediksi = model.predict(
            [seq_cv, seq_job],
            batch_size=8,
            verbose=0
        ).flatten()

        # 7. Urutkan skor dan ambil Top 20 Index
        # argsort() mengurutkan dari kecil ke besar, [::-1] membaliknya, [:20] mengambil 20 teratas
        top_20_index = np.argsort(skor_prediksi)[::-1][:20]

        # 8. Susun format response final
        hasil_rekomendasi = []
        for urutan, idx in enumerate(top_20_index):
            loker_obj = semua_loker[idx]
            skor = float(skor_prediksi[idx])
            
            # Ubah object Loker menjadi dictionary (JSON) menggunakan serializer
            loker_data = LokerSerializer(loker_obj).data
            
            hasil_rekomendasi.append({
                "ranking": urutan + 1,
                "skor_kecocokan": round(skor, 4), # Dibulatkan 4 desimal agar rapi
                "detail_loker": loker_data
            })

        return Response({
            "pesan": "Inferensi berhasil",
            "total_lowongan_dianalisis": jumlah_lowongan,
            "rekomendasi": hasil_rekomendasi
        }, status=status.HTTP_200_OK)