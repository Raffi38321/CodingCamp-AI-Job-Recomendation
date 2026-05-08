from django.db import models

class Loker(models.Model):
    id_loker = models.CharField(max_length=100, primary_key=True)
    judul = models.CharField(max_length=255, null=True, blank=True)
    industri = models.CharField(max_length=255, null=True, blank=True)
    tipe = models.CharField(max_length=100, null=True, blank=True)
    kategori = models.CharField(max_length=255, null=True, blank=True)
    tanggal_post = models.CharField(max_length=100, null=True, blank=True)
    berlaku_hingga = models.CharField(max_length=100, null=True, blank=True)
    perusahaan = models.CharField(max_length=255, null=True, blank=True)
    website_perusahaan = models.TextField(null=True, blank=True)
    logo_perusahaan = models.TextField(null=True, blank=True)
    alamat = models.TextField(null=True, blank=True)
    kota = models.CharField(max_length=100, null=True, blank=True)
    provinsi = models.CharField(max_length=100, null=True, blank=True)
    negara = models.CharField(max_length=100, null=True, blank=True)
    latitude = models.CharField(max_length=100, null=True, blank=True)
    longitude = models.CharField(max_length=100, null=True, blank=True)
    gaji_min = models.CharField(max_length=100, null=True, blank=True)
    gaji_max = models.CharField(max_length=100, null=True, blank=True)
    gaji_currency = models.CharField(max_length=50, null=True, blank=True)
    gaji_unit = models.CharField(max_length=50, null=True, blank=True)
    skills = models.TextField(null=True, blank=True)
    pengalaman_bulan = models.CharField(max_length=100, null=True, blank=True)
    pendidikan = models.CharField(max_length=255, null=True, blank=True)
    deskripsi = models.TextField(null=True, blank=True)
    tentang_perusahaan = models.TextField(null=True, blank=True)
    benefit = models.TextField(null=True, blank=True)
    link = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.judul} - {self.perusahaan}"

    class Meta:
        db_table = 'loker' # Memaksa nama tabel di PostgreSQL menjadi 'loker'