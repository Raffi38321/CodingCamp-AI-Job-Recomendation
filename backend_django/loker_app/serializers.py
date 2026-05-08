from rest_framework import serializers
from .models import Loker

class LokerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loker
        fields = '__all__' # Ini akan otomatis mengambil semua atribut yang ada di model Loker