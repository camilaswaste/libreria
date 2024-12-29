from django import forms
from django.forms import inlineformset_factory

from .models import DetalleMovimiento, Movimiento


class MovimientoForm(forms.ModelForm):
    class Meta:
        model = Movimiento
        fields = ['bodega_origen', 'bodega_destino']
        widgets = {
            'bodega_origen': forms.Select(attrs={'class': 'form-control'}),
            'bodega_destino': forms.Select(attrs={'class': 'form-control'}),
        }

class DetalleMovimientoForm(forms.ModelForm):
    class Meta:
        model = DetalleMovimiento
        fields = ['producto', 'cantidad']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
        }

DetalleMovimientoFormSet = inlineformset_factory(
    Movimiento, 
    DetalleMovimiento, 
    form=DetalleMovimientoForm,
    extra=1,
    can_delete=True
)

