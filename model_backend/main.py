from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import List
import fitz
import re
import numpy as np
import pandas as pd
import tensorflow as tf
import pickle
from tensorflow.keras.preprocessing.sequence import pad_sequences

app = FastAPI(
    title="Job Recommendation API",
    description="API untuk rekomendasi lowongan kerja berdasarkan CV PDF menggunakan Siamese BiLSTM",
    version="1.0.0"
)

model = tf.keras.models.load_model("models/model_rekomendasi_loker.keras")

with open("models/tokenizer_loker.pkl", "rb") as f:
    tokenizer = pickle.load(f)

df = pd.read_csv("datas/data_backend.csv")

MAX_LEN = 150

class RecommendationItem(BaseModel):
    judul: str
    perusahaan: str
    lokasi: str
    Skills: str
    skor: float


class RecommendationResponse(BaseModel):
    status: str
    rekomendasi: List[RecommendationItem]

def basic_clean(text):
    text = text.lower()
    text = re.sub(r'<.*?>', ' ', text)
    text = re.sub(r'[^a-z0-9\s:/_\-\+\.]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def extract_text_from_pdf(file_bytes: bytes) -> str:
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text.strip()

@app.post(
    "/recommend-from-cv",
    response_model=RecommendationResponse,
    summary="Rekomendasi pekerjaan dari CV",
    description="""
Upload file CV PDF lalu sistem akan:
- Mengekstrak isi CV
- Membersihkan teks
- Membandingkan CV dengan seluruh lowongan kerja
- Mengembalikan top rekomendasi pekerjaan

Format file yang didukung:
- PDF
"""
)
async def recommend_from_cv(file: UploadFile = File(...)):

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="File harus PDF"
        )

    # Extract PDF
    file_bytes = await file.read()
    raw_text = extract_text_from_pdf(file_bytes)

    if not raw_text:
        raise HTTPException(
            status_code=422,
            detail="Gagal membaca CV"
        )

    # Cleaning
    cv_text = basic_clean(raw_text)

    # Ambil semua job
    semua_job = df['text_gabungan'].tolist()
    jumlah_job = len(semua_job)

    # Gandakan CV
    cv_list = [cv_text] * jumlah_job

    # Tokenize
    seq_cv = pad_sequences(
        tokenizer.texts_to_sequences(cv_list),
        maxlen=MAX_LEN,
        padding='post'
    )

    seq_job = pad_sequences(
        tokenizer.texts_to_sequences(semua_job),
        maxlen=MAX_LEN,
        padding='post'
    )

    # Predict
    skor = model.predict([seq_cv, seq_job], verbose=0).flatten()

    # Ranking
    index_sorted = np.argsort(skor)[::-1]

    hasil = []

    for i in index_sorted[:5]:
        hasil.append({
            "judul": df.loc[i, "Judul"],
            "perusahaan": df.loc[i, "Industri"],
            "lokasi": df.loc[i, "Kota"],
            "Skills": df.loc[i, "Skills"],
            "skor": float(skor[i])
        })

    return {
        "status": "success",
        "rekomendasi": hasil
    }