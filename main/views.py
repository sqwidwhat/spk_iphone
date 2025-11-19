from django.shortcuts import render
from .models import Kriteria, Iphone
from decimal import Decimal # Tambahkan import ini untuk perhitungan yang akurat
from django.shortcuts import render, get_object_or_404, redirect
from .forms import ContactForm  # Import form
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail

def index(request):
    semua_kriteria = Kriteria.objects.all()
    semua_iphone = Iphone.objects.all()
    return render(request, 'index.html', {
        'kriteria': semua_kriteria,
        'semua_iphone': semua_iphone,
    })


def rekomendasi_saw(request):
    semua_kriteria = Kriteria.objects.all()
    semua_iphone = Iphone.objects.all()

    # Mapping nama kriteria ke atribut model Iphone
    atribut_mapping = {
        'Harga': 'harga',
        'Kamera': 'kamera',
        'Memori Internal': 'memori',
        'Kondisi Fisik': 'kondisi_fisik',
        'Kondisi Baterai': 'kondisi_baterai',
    }

    if request.method == 'POST':
        # 1. Ambil bobot dari POST request
        bobot_konsumen = {}
        for kriteria in semua_kriteria:
            bobot_konsumen[kriteria.nama] = Decimal(request.POST.get(kriteria.nama, 0))

        # 2. Normalisasi Bobot (total = 1)
        total_bobot = sum(bobot_konsumen.values())
        if total_bobot > 0:
            for kriteria_nama in bobot_konsumen:
                bobot_konsumen[kriteria_nama] /= total_bobot

        # 3. Hitung Nilai Min/Max untuk Normalisasi
        min_max_values = {}
        
        for kriteria in semua_kriteria:
            atribut_nama = atribut_mapping.get(kriteria.nama, kriteria.nama.lower())
            nilai_list = [Decimal(getattr(iphone, atribut_nama)) for iphone in semua_iphone]
            
            if kriteria.tipe == 'benefit':
                min_max_values[kriteria.nama] = max(nilai_list) if nilai_list else Decimal(1)
            else: # 'cost'
                min_max_values[kriteria.nama] = min(nilai_list) if nilai_list else Decimal(1)

        # 4. Hitung Nilai Preferensi (Skor Akhir)
        hasil_saw = []
        for iphone in semua_iphone:
            skor_preferensi = Decimal(0)
            
            for kriteria in semua_kriteria:
                atribut_nama = atribut_mapping.get(kriteria.nama, kriteria.nama.lower())
                nilai_kriteria = Decimal(getattr(iphone, atribut_nama))
                bobot = bobot_konsumen.get(kriteria.nama, Decimal(0))
                nilai_normal = Decimal(0)

                # Normalisasi Nilai (rij)
                if kriteria.tipe == 'benefit':
                    max_val = min_max_values[kriteria.nama]
                    if max_val > 0:
                        nilai_normal = nilai_kriteria / max_val
                else: # 'cost'
                    min_val = min_max_values[kriteria.nama]
                    if nilai_kriteria > 0:
                        nilai_normal = min_val / nilai_kriteria 

                # Perhitungan Skor Preferensi (Vi) = SUM (rij * Wj)
                skor_preferensi += nilai_normal * bobot
            
            hasil_saw.append({'iphone': iphone, 'skor': float(skor_preferensi)}) 
        
        # 5. Urutkan hasil dari skor tertinggi
        hasil_saw.sort(key=lambda x: x['skor'], reverse=True)

        return render(request, 'hasil.html', {'hasil_saw': hasil_saw})

    # GET method - tampilkan halaman input bobot
    return render(request, 'input.html', {'kriteria': semua_kriteria})

def detail_iphone(request, id):
    iphone = Iphone.objects.get(id=id)
    return render(request, 'detail_iphone.html', {'iphone': iphone})


# TAMPILAN UNTUK TENTANG
def tentang(request):
    return render(request, 'tentang.html')

# TAMBAHKAN VIEW KONTAK INI
def kontak(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Simpan ke database
            contact_message = form.save()
            
            # Kirim email
            subject = f"Pesan dari iPhone Recommender: {contact_message.subject}"
            message = f"""
Nama: {contact_message.name}
Email: {contact_message.email}
Subjek: {contact_message.subject}

Pesan:
{contact_message.message}

---
Pesan ini dikirim melalui iPhone Recommender System.
            """
            
            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    ['andikamelawi.net11@gmail.com'],  # Email penerima
                    fail_silently=False,
                )
                messages.success(request, 'Pesan Anda telah berhasil dikirim! Kami akan membalas dalam 1x24 jam.')
                
            except Exception as e:
                # Log error untuk debugging
                print(f"❌ Error mengirim email: {e}")
                # Tetap simpan ke database meski email gagal
                messages.warning(request, 'Pesan berhasil disimpan. Namun terjadi gangguan pada sistem email. Kami akan tetap menindaklanjuti pesan Anda.')
            
            return redirect('kontak')
        else:
            messages.error(request, 'Terjadi kesalahan. Silakan periksa kembali form Anda.')
    else:
        form = ContactForm()
    
    return render(request, 'kontak.html', {'form': form})