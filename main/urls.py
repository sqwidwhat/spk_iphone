# main/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('rekomendasi_saw/', views.rekomendasi_saw, name='rekomendasi'), 
    path('detail/<int:id>/', views.detail_iphone, name='detail_iphone'),  # 🔹 Tambah ini
    path('tentang/', views.tentang, name='tentang'), 
    path('kontak/', views.kontak, name='kontak'), 
]