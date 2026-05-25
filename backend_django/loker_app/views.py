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

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ==========================================
# LOAD MODEL, TOKENIZER & CACHE DATA LOKER
# Semua ini hanya dijalankan SEKALI saat server start
# ==========================================
model     = None
tokenizer = None

MODEL_PATH     = os.path.join(settings.BASE_DIR, './../model_hasil/model_rekomendasi_3.keras')
TOKENIZER_PATH = os.path.join(settings.BASE_DIR, './../model_hasil/tokenizer_loker3.pkl')
MAX_LEN        = 299

print("Sedang memuat ML Model dan Tokenizer ke dalam memori...")
try:
    model = load_model(MODEL_PATH, compile=False)
    with open(TOKENIZER_PATH, 'rb') as f:
        print("Memuat tokenizer...")
        tokenizer = pickle.load(f)
    print("Model berhasil dimuat!")
except Exception as e:
    print(f"Gagal memuat model: {e}")

# ── Cache data loker ──────────────────────────────────────────────────────────
# Dijalankan sekali saat startup; tidak berubah selama server hidup.
print("Memuat dan meng-cache data loker...")
try:
    _semua_loker = list(Loker.objects.all())

    # Teks gabungan untuk input model (seq_job)
    _semua_teks_lowongan = []
    for loker in _semua_loker:
        industri  = loker.industri  or ""
        kategori  = loker.kategori  or ""
        pendidikan = loker.pendidikan or ""
        tipe      = loker.tipe      or ""
        lokasi    = f"{loker.kota or ''} {loker.provinsi or ''}".strip()
        skills    = loker.skills    or ""
        deskripsi = loker.deskripsi or ""
        teks_gabungan = f"{industri} {kategori} {pendidikan} {tipe} {lokasi} {skills} {deskripsi}".strip()
        _semua_teks_lowongan.append(teks_gabungan)

    # Pre-tokenisasi & padding semua loker → disimpan sebagai numpy array
    if tokenizer is not None:
        _seq_job_cache = pad_sequences(
            tokenizer.texts_to_sequences(_semua_teks_lowongan),
            maxlen=MAX_LEN,
            padding='post'
        )
    else:
        _seq_job_cache = None

    # Pre-serialize semua loker → list of dict, siap masuk response
    _loker_serialized = [LokerSerializer(l).data for l in _semua_loker]

    # Pre-fit TF-IDF pada judul loker saja; saat request tinggal transform 1 judul CV
    _daftar_judul_loker = [loker.judul or "" for loker in _semua_loker]
    _tfidf = TfidfVectorizer(ngram_range=(1, 2))
    _tfidf_matrix_loker = _tfidf.fit_transform(_daftar_judul_loker)  # shape: (n_loker, vocab)

    print(f"Cache loker selesai: {len(_semua_loker)} lowongan.")
except Exception as e:
    print(f"Gagal meng-cache data loker: {e}")
    _semua_loker          = []
    _semua_teks_lowongan  = []
    _seq_job_cache        = None
    _loker_serialized     = []
    _daftar_judul_loker   = []
    _tfidf                = None
    _tfidf_matrix_loker   = None


# ── ViewSet CRUD ──────────────────────────────────────────────────────────────
class LokerViewSet(viewsets.ModelViewSet):
    queryset         = Loker.objects.all()
    serializer_class = LokerSerializer


# ── Inferensi ─────────────────────────────────────────────────────────────────
class InferensiAPIView(APIView):

    @extend_schema(
        request=inline_serializer(
            name="RequestCV",
            fields={
                "title":      serializers.CharField(),
                "industri":   serializers.CharField(),
                "kategori":   serializers.CharField(),
                "pendidikan": serializers.CharField(),
                "tipe":       serializers.CharField(),
                "skills":     serializers.CharField(),
            }
        ),
        description="Menerima teks CV, mencocokkannya dengan semua loker, dan mengembalikan Top 30."
    )
    def post(self, request):
        if model is None:
            return Response(
                {"error": "Model ML gagal dimuat. Silakan cek terminal server Django."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        if tokenizer is None:
            return Response(
                {"error": "Tokenizer gagal dimuat."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        if not _semua_loker:
            return Response({"error": "Database loker masih kosong"}, status=status.HTTP_404_NOT_FOUND)

        # 1. Ambil input CV dari user
        text_cv_title = request.data.get('title', '')
        text_cv_user  = (
            request.data.get('industri',   '') + " " +
            request.data.get('kategori',   '') + " " +
            request.data.get('pendidikan', '') + " " +
            request.data.get('tipe',       '') + " " +
            request.data.get('skills',     '')
        )
        if not text_cv_title or not text_cv_user.strip():
            return Response({"error": "Semua field wajib diisi"}, status=status.HTTP_400_BAD_REQUEST)

        jumlah_lowongan = len(_semua_loker)

        # 2. Tokenisasi CV (hanya 1 vektor, lalu tile ke jumlah loker)
        seq_cv_single = pad_sequences(
            tokenizer.texts_to_sequences([text_cv_user]),
            maxlen=MAX_LEN,
            padding='post'
        )                                              # shape: (1, MAX_LEN)
        seq_cv = np.tile(seq_cv_single, (jumlah_lowongan, 1))  # shape: (n, MAX_LEN)

        # 3. Gunakan seq_job yang sudah di-cache
        seq_job = _seq_job_cache                       # shape: (n, MAX_LEN)

        # 4. Prediksi — batch_size besar agar lebih efisien
        prediksi_model = model.predict(
            [seq_cv, seq_job],
            batch_size=128,
            verbose=0
        ).flatten()

        # 5. TF-IDF judul — transform hanya 1 vektor CV, lalu cosine similarity
        vec_cv_title    = _tfidf.transform([text_cv_title])          # shape: (1, vocab)
        skor_tfidf_judul = cosine_similarity(vec_cv_title, _tfidf_matrix_loker).flatten()

        # 6. Gabungkan skor
        skor_prediksi = (prediksi_model * 0.5) + (skor_tfidf_judul * 0.5)

        # 7. Ambil Top 30
        top_30_index = np.argsort(skor_prediksi)[::-1][:30]

        # 8. Susun response — gunakan data yang sudah di-serialize
        hasil_rekomendasi = [
            {
                "ranking":        urutan + 1,
                "skor_kecocokan": round(float(skor_prediksi[idx]), 4),
                "detail_loker":   _loker_serialized[idx],
            }
            for urutan, idx in enumerate(top_30_index)
        ]

        return Response({
            "pesan":                    "Inferensi berhasil",
            "total_lowongan_dianalisis": jumlah_lowongan,
            "rekomendasi":              hasil_rekomendasi,
        }, status=status.HTTP_200_OK)
