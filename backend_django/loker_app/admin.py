from django.contrib import admin
from .models import Loker

# Mendaftarkan model Loker ke panel admin
@admin.register(Loker)
class LokerAdmin(admin.ModelAdmin):
    # Kolom apa saja yang mau ditampilkan di halaman list
    list_display = ('id_loker', 'judul', 'perusahaan', 'kota')
    # Menambahkan fitur pencarian (search box)
    search_fields = ('judul', 'perusahaan', 'kategori')
    
