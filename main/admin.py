from django.contrib import admin
from django.utils.html import format_html
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin, ImportMixin, ExportMixin
from import_export.widgets import ForeignKeyWidget
from .models import Kriteria, Iphone, ContactMessage

# ==================== RESOURCES UNTUK IMPORT/EXPORT ====================

class IphoneResource(resources.ModelResource):
    # Jika butuh custom field mapping
    kode = fields.Field(attribute='kode', column_name='kode')
    nama = fields.Field(attribute='nama', column_name='nama')
    harga = fields.Field(attribute='harga', column_name='harga')
    kamera = fields.Field(attribute='kamera', column_name='kamera')
    memori = fields.Field(attribute='memori', column_name='memori')
    kondisi_fisik = fields.Field(attribute='kondisi_fisik', column_name='kondisi_fisik')
    kondisi_baterai = fields.Field(attribute='kondisi_baterai', column_name='kondisi_baterai')
    deskripsi = fields.Field(attribute='deskripsi', column_name='deskripsi')
    gambar = fields.Field(attribute='gambar', column_name='gambar')

    class Meta:
        model = Iphone
        skip_unchanged = True
        report_skipped = True
        import_id_fields = ('kode',)  # Gunakan kode sebagai identifier
        fields = ('kode', 'nama', 'harga', 'kamera', 'memori', 'kondisi_fisik', 'kondisi_baterai', 'deskripsi', 'gambar')
        export_order = fields

    def before_import_row(self, row, **kwargs):
        """Hook untuk preprocessing data sebelum import"""
        # Auto-generate kode jika tidak ada
        if not row.get('kode') and row.get('nama'):
            base_name = row['nama'].replace(' ', '').replace('iPhone', 'IP')
            memori = row.get('memori', 64)
            kondisi = row.get('kondisi_fisik', 80)
            row['kode'] = f"{base_name}-{memori}-{kondisi}"

class KriteriaResource(resources.ModelResource):
    class Meta:
        model = Kriteria
        import_id_fields = ('nama',)

class ContactMessageResource(resources.ModelResource):
    class Meta:
        model = ContactMessage
        fields = ('name', 'email', 'subject', 'message', 'created_at', 'is_read')
        export_only = True  # Hanya untuk export, tidak untuk import

# ==================== ADMIN CLASSES YANG DIPERBARUI ====================

# Daftarkan Model Kriteria
@admin.register(Kriteria)
class KriteriaAdmin(ImportExportModelAdmin): 
    resource_class = KriteriaResource
    list_display = ('nama', 'tipe_badge', 'jumlah_iphone')
    list_filter = ('tipe',)
    search_fields = ('nama',)
    ordering = ('nama',)
    
    def tipe_badge(self, obj):
        if obj.tipe == 'benefit':
            color = 'success'
            icon = '↗'
        else:
            color = 'danger'
            icon = '↘'
        return format_html(
            '<span class="badge bg-{}">{}{}</span>',
            color, icon, obj.tipe.upper()
        )
    tipe_badge.short_description = 'Tipe Kriteria'
    
    def jumlah_iphone(self, obj):
        count = Iphone.objects.count()
        return format_html(
            '<span class="badge bg-info">{}</span>',
            "{} iPhone".format(count)
        )
    jumlah_iphone.short_description = 'Total iPhone'

# Daftarkan Model Iphone
@admin.register(Iphone)
class IphoneAdmin(ImportExportModelAdmin): 
    resource_class = IphoneResource
    list_display = (
        'kode',  #
        'nama', 
        'harga_format', 
        'kamera_badge', 
        'memori_badge', 
        'kondisi_fisik_badge', 
        'kondisi_baterai_badge',
        'gambar_preview'
    )
    list_filter = ('memori', 'kondisi_fisik', 'kondisi_baterai')
    search_fields = ('kode', 'nama', 'deskripsi')  # ⭐ TAMBAHKAN KODE DI SEARCH
    readonly_fields = ('gambar_preview_large',)
    list_per_page = 20
    
    # Custom fields untuk list display
    def harga_format(self, obj):
        harga_formatted = "Rp {:,}".format(int(obj.harga)).replace(",", ".")
        return format_html(
            '<strong>{}</strong>',
            harga_formatted
        )
    harga_format.short_description = 'Harga'
    
    def kamera_badge(self, obj):
        # Ubah dari MP menjadi rating
        if obj.kamera >= 95:
            color = 'success'
            label = 'Excellent'
        elif obj.kamera >= 90:
            color = 'info'
            label = 'Very Good'
        elif obj.kamera >= 85:
            color = 'warning'
            label = 'Good'
        else:
            color = 'secondary'
            label = 'Standard'
        return format_html(
            '<span class="badge bg-{}">{} - {}</span>',
            color, obj.kamera, label
        )
    kamera_badge.short_description = 'Kamera'
    
    def memori_badge(self, obj):
        colors = {
            64: 'secondary',
            128: 'info', 
            256: 'primary',
            512: 'success'
        }
        color = colors.get(obj.memori, 'warning')
        return format_html(
            '<span class="badge bg-{}">{} GB</span>',
            color, obj.memori
        )
    memori_badge.short_description = 'Memori Internal'
    
    def kondisi_fisik_badge(self, obj):
        if obj.kondisi_fisik >= 90:
            color = 'success'
            label = 'Sangat Baik'
        elif obj.kondisi_fisik >= 80:
            color = 'info'
            label = 'Baik'
        elif obj.kondisi_fisik >= 70:
            color = 'warning'
            label = 'Cukup'
        else:
            color = 'danger'
            label = 'Kurang'
        return format_html(
            '<span class="badge bg-{}">{}% - {}</span>',
            color, obj.kondisi_fisik, label
        )
    kondisi_fisik_badge.short_description = 'Kondisi Fisik'
    
    def kondisi_baterai_badge(self, obj):
        if obj.kondisi_baterai >= 90:
            color = 'success'
            label = 'Sangat Baik'
        elif obj.kondisi_baterai >= 80:
            color = 'info'
            label = 'Baik'
        elif obj.kondisi_baterai >= 70:
            color = 'warning'
            label = 'Cukup'
        else:
            color = 'danger'
            label = 'Kurang'
        return format_html(
            '<span class="badge bg-{}">{}% - {}</span>',
            color, obj.kondisi_baterai, label
        )
    kondisi_baterai_badge.short_description = 'Kondisi Baterai'
    
    def gambar_preview(self, obj):
        if obj.gambar:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 5px;" />',
                obj.gambar
            )
        return format_html('<span class="text-muted">No Image</span>')
    gambar_preview.short_description = 'Gambar'
    
    def gambar_preview_large(self, obj):
        if obj.gambar:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 300px; border-radius: 10px;" />',
                obj.gambar
            )
        return format_html('<span class="text-muted">Tidak ada gambar</span>')
    gambar_preview_large.short_description = 'Preview Gambar'
    
    # Custom actions
    def mark_high_condition(self, request, queryset):
        updated = queryset.update(kondisi_fisik=95, kondisi_baterai=95)
        self.message_user(request, '{} iPhone ditandai sebagai kondisi tinggi.'.format(updated))
    mark_high_condition.short_description = "Tandai kondisi tinggi"
    
    actions = [mark_high_condition]

# Daftarkan Model ContactMessage
@admin.register(ContactMessage)
class ContactMessageAdmin(ExportMixin, admin.ModelAdmin):  # ⭐ HANYA EXPORT, TIDAK IMPORT
    resource_class = ContactMessageResource
    list_display = (
        'name', 
        'email_link', 
        'subject_truncated', 
        'created_at_format', 
        'is_read_badge'
    )
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at', 'name', 'email', 'subject', 'message', 'preview_message')
    list_per_page = 25
    
    # Custom fields
    def email_link(self, obj):
        return format_html(
            '<a href="mailto:{}">{}</a>',
            obj.email, obj.email
        )
    email_link.short_description = 'Email'
    
    def subject_truncated(self, obj):
        if len(obj.subject) > 50:
            return "{}...".format(obj.subject[:50])
        return obj.subject
    subject_truncated.short_description = 'Subjek'
    
    def created_at_format(self, obj):
        from django.utils import timezone
        import datetime
        
        if obj.created_at.date() == timezone.now().date():
            return format_html(
                '<span style="color: #28a745;">Hari ini, {}</span>',
                obj.created_at.strftime('%H:%M')
            )
        elif obj.created_at.date() == (timezone.now() - datetime.timedelta(days=1)).date():
            return format_html(
                '<span style="color: #fd7e14;">Kemarin, {}</span>',
                obj.created_at.strftime('%H:%M')
            )
        else:
            return obj.created_at.strftime('%d %b %Y, %H:%M')
    created_at_format.short_description = 'Dikirim'
    
    def is_read_badge(self, obj):
        if obj.is_read:
            return format_html(
                '<span class="badge bg-success">Dibaca</span>'
            )
        return format_html(
            '<span class="badge bg-warning text-dark">Belum dibaca</span>'
        )
    is_read_badge.short_description = 'Status'
    
    def preview_message(self, obj):
        return format_html(
            '''
            <div style="background: #f8f9fa; padding: 15px; border-radius: 5px; border-left: 4px solid #007bff;">
                <strong>Pesan:</strong><br>
                {}
            </div>
            ''',
            obj.message.replace('\n', '<br>')
        )
    preview_message.short_description = 'Preview Pesan'
    
    # Custom view untuk pesan
    fieldsets = (
        ('Informasi Pengirim', {
            'fields': ('name', 'email', 'subject', 'created_at')
        }),
        ('Isi Pesan', {
            'fields': ('preview_message',),
            'classes': ('collapse', 'wide')
        }),
        ('Status', {
            'fields': ('is_read',)
        }),
    )
    
    # Custom actions
    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, '{} pesan ditandai sebagai sudah dibaca.'.format(updated))
    mark_as_read.short_description = "Tandai sebagai sudah dibaca"
    
    def mark_as_unread(self, request, queryset):
        updated = queryset.update(is_read=False)
        self.message_user(request, '{} pesan ditandai sebagai belum dibaca.'.format(updated))
    mark_as_unread.short_description = "Tandai sebagai belum dibaca"
    
    actions = [mark_as_read, mark_as_unread]