# forms.py
from django import forms
from .models import Contacto, Libro
from django.contrib.auth.decorators import login_required

class ContactoForm(forms.ModelForm):
    class Meta:
        model = Contacto
        fields = ['nombre', 'correo', 'telefono', 'comentario']
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'input'}),
            'correo': forms.EmailInput(attrs={'class':'input'}),
            'telefono': forms.TextInput(attrs={'class':'input'}),
            'comentario': forms.Textarea(attrs={'class':'textarea'}),
        }
@login_required       
class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = '__all__'  # Incluye todos los campos automáticamente
        widgets = {
            'titulo': forms.TextInput(attrs={'placeholder': 'Ingrese el título del libro'}),
            'autor': forms.TextInput(attrs={'placeholder': 'Ingrese el autor'}),
            'fecha_publicacion': forms.DateInput(attrs={'type': 'date'}),
        }
        help_texts = {
            'saga': '¿El libro es parte de una saga?',
        }

