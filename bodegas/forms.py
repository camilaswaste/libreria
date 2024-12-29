from django import forms

from .models import Bodega, BodegaProducto


class BodegaForm(forms.ModelForm):
    class Meta:
        model = Bodega
        fields = ['codigo_bodega', 'nombre_bodega', 'ubicacion', 'jefe_bodega']
        
    def clean_codigo_bodega(self):
        codigo = self.cleaned_data['codigo_bodega']
        if len(codigo) < 3:
            raise forms.ValidationError('El código debe tener al menos 3 caracteres')
        return codigo

class BodegaProductoForm(forms.ModelForm):
    class Meta:
        model = BodegaProducto
        fields = ['producto', 'cantidad']
        
    def clean_cantidad(self):
        cantidad = self.cleaned_data['cantidad']
        if cantidad < 0:
            raise forms.ValidationError('La cantidad no puede ser negativa')
        return cantidad