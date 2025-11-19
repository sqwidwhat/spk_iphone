from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nama Lengkap Anda'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control', 
                'placeholder': 'email@contoh.com'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Subjek pesan'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Tulis pesan Anda di sini...',
                'rows': 5
            }),
        }
        labels = {
            'name': 'Nama Lengkap',
            'email': 'Alamat Email', 
            'subject': 'Subjek Pesan',
            'message': 'Isi Pesan'
        }