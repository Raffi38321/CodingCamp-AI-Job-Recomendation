import os
import django
import csv
import uuid

# 1. Konfigurasi agar script ini mengenali environment Django kamu
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

# 2. Import model Loker setelah setup selesai
from loker_app.models import Loker

def jalankan_import():
    file_path = './../data_untuk_raw_backend.csv'
    
    print("Mulai membaca file CSV...")
    
    # Buka file CSV
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        jumlah_data = 0
        for row in reader:
            # Ambil ID dari kolom 'id_loker' atau 'Unnamed: 0', jika tidak ada pakai counter
            # id_baris = row.get('id_loker') or row.get('Unnamed: 0') or str(jumlah_data)
            id_uuid = str(uuid.uuid4())  # Generate UUID unik untuk setiap baris
            
            # Buat dan simpan data ke database
            Loker.objects.create(
                id_loker=id_uuid,
                judul=row.get('Judul', ''),
                industri=row.get('Industri', ''),
                tipe=row.get('Tipe', ''),
                kategori=row.get('Kategori', ''),
                tanggal_post=row.get('Tanggal_Post', ''),
                berlaku_hingga=row.get('Berlaku_Hingga', ''),
                perusahaan=row.get('Perusahaan', ''),
                website_perusahaan=row.get('Website_Perusahaan', ''),
                logo_perusahaan=row.get('Logo_Perusahaan', ''),
                alamat=row.get('Alamat', ''),
                kota=row.get('Kota', ''),
                provinsi=row.get('Provinsi', ''),
                negara=row.get('Negara', ''),
                latitude=row.get('Latitude', ''),
                longitude=row.get('Longitude', ''),
                gaji_min=row.get('Gaji_Min', ''),
                gaji_max=row.get('Gaji_Max', ''),
                gaji_currency=row.get('Gaji_Currency', ''),
                gaji_unit=row.get('Gaji_Unit', ''),
                skills=row.get('Skills', ''),
                pengalaman_bulan=row.get('Pengalaman_Bulan', ''),
                pendidikan=row.get('Pendidikan', ''),
                deskripsi=row.get('Deskripsi', ''),
                tentang_perusahaan=row.get('Tentang_Perusahaan', ''),
                benefit=row.get('Benefit', ''),
                link=row.get('Link', '')
            )
            jumlah_data += 1
            
            # Print progres setiap 100 data agar kita tahu scriptnya tidak macet
            if jumlah_data % 100 == 0:
                print(f"Sedang memproses... {jumlah_data} data berhasil dimasukkan.")
                
    print(f"SELESAI! Total {jumlah_data} data lowongan berhasil di-import ke Vercel Postgres.")

if __name__ == '__main__':
    jalankan_import()