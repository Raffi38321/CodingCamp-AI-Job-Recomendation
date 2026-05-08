from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LokerViewSet, InferensiAPIView

# Router ini akan otomatis membuatkan URL untuk endpoint CRUD kita
router = DefaultRouter()
router.register(r'loker', LokerViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # URL untuk endpoint inferensi
    path('inferensi/', InferensiAPIView.as_view(), name='inferensi'),
]