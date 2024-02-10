from django import forms
from .models import Productos

class ProductosForm(forms.ModelForm):
    class Meta:
        model = Productos
        fields = ['nombre', 'descripcion', 'cantidad', 'precio', 'disponibilidad', 'imagen']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el Nombre del Producto'
            }),
            'descripcion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese la Descripción del Producto'
            }),
            'cantidad': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese la Cantidad del Producto'
            }),
            'precio': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el Precio del Producto'
            }),
            'disponibilidad': forms.CheckboxInput(attrs={
                'class': 'form-control',
            }),
            'imagen': forms.FileInput(attrs={
                'class': 'form-control',
            }),
        }
        error_messages = {
            'imagen': {
                'required': 'Por favor, cargue una imagen para el producto.',
            },
        }