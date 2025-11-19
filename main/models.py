from django.db import models

# Model untuk Kriteria
class Kriteria(models.Model):
    nama = models.CharField(max_length=50)
    tipe = models.CharField(max_length=10)

    def __str__(self):
        return self.nama

# Model untuk iPhone
class Iphone(models.Model):
    kode = models.CharField(max_length=50, unique=True, verbose_name="Kode Produk")
    nama = models.CharField(max_length=100)
    harga = models.DecimalField(max_digits=10, decimal_places=2)
    kamera = models.IntegerField()
    memori = models.IntegerField(default=64)
    kondisi_fisik = models.IntegerField()
    kondisi_baterai = models.IntegerField()
    deskripsi = models.TextField(blank=True, null=True)
    gambar = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.kode} - {self.nama} ({self.memori}GB)"

    class Meta:
        verbose_name = "iPhone"
        verbose_name_plural = "iPhone"
    
# Model untuk Contact
class ContactMessage(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nama Lengkap")
    email = models.EmailField(verbose_name="Email")
    subject = models.CharField(max_length=200, verbose_name="Subjek")
    message = models.TextField(verbose_name="Pesan")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Dikirim pada")
    is_read = models.BooleanField(default=False, verbose_name="Sudah Dibaca")

    def __str__(self):
        return f"{self.name} - {self.subject}"

    class Meta:
        db_table = 'contact_messages'
        verbose_name = 'Pesan Kontak'
        verbose_name_plural = 'Pesan Kontak'
        ordering = ['-created_at']
