# test_email_smtp.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spk_iphone.settings')
django.setup()

from django.core.mail import send_mail

print("🚀 Mengirim email test via SMTP...")

try:
    send_mail(
        '🎉 TEST BERHASIL - iPhone Recommender',
        '''
Selamat! 

Konfigurasi email SMTP Anda BERHASIL!

✅ Email ini dikirim melalui Gmail SMTP
✅ Form kontak website sekarang bisa kirim email sungguhan
✅ Semua pesan dari user akan masuk ke inbox Anda

Detail Pesan Test:
- Dari: iPhone Recommender System
- Ke: andikamelawi.net11@gmail.com  
- Metode: Django SMTP + Gmail

Sekarang coba isi form kontak di website!

Regards,
Sistem iPhone Recommender
        ''',
        'iPhone Recommender <noreply@iphonerecommender.com>',
        ['andikamelawi.net11@gmail.com'],
        fail_silently=False,
    )
    print("✅ EMAIL TEST BERHASIL DIKIRIM!")
    print("📧 Cek inbox: andikamelawi.net11@gmail.com")
    print("📨 Jangan lupa cek folder SPAM juga!")
    
except Exception as e:
    print("❌ GAGAL MENGIRIM EMAIL:")
    print(f"Error: {e}")
    print("\n🔧 Kemungkinan masalah:")
    print("1. App Password salah")
    print("2. 2FA belum diaktifkan")
    print("3. Less secure apps blocked")