from django import forms

from .models import Autor, Editorial, Producto


class EditorialForm(forms.ModelForm):
    class Meta:
        model = Editorial
        fields = ['nombre_editorial', 'direccion', 'telefono']
        widgets = {
            'nombre_editorial': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_nombre_editorial(self):
        nombre_editorial = self.cleaned_data.get('nombre_editorial')
        if Editorial.objects.filter(nombre_editorial__iexact=nombre_editorial).exists():
            raise forms.ValidationError("Esta editorial ya existe en el sistema.")
        return nombre_editorial

class AutorForm(forms.ModelForm):
    class Meta:
        model = Autor
        fields = ['nombre_autor', 'nacionalidad']
        widgets = {
            'nombre_autor': forms.TextInput(attrs={'class': 'form-control'}),
            'nacionalidad': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_nombre_autor(self):
        nombre_autor = self.cleaned_data.get('nombre_autor')
        if Autor.objects.filter(nombre_autor__iexact=nombre_autor).exists():
            raise forms.ValidationError("Este autor ya existe en el sistema.")
        return nombre_autor

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'tipo', 'editorial', 'autores', 'precio']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'editorial': forms.Select(attrs={'class': 'form-control'}),
            'autores': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
        }

