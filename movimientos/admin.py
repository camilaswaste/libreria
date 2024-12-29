from django.contrib import admin

from .models import DetalleMovimiento, Movimiento


class DetalleMovimientoInline(admin.TabularInline):
    model = DetalleMovimiento
    extra = 1

@admin.register(Movimiento)
class MovimientoAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha_movimiento', 'bodega_origen', 'bodega_destino', 'usuario')
    list_filter = ('fecha_movimiento', 'bodega_origen', 'bodega_destino')
    search_fields = ('bodega_origen__nombre_bodega', 'bodega_destino__nombre_bodega')
    inlines = [DetalleMovimientoInline]

@admin.register(DetalleMovimiento)
class DetalleMovimientoAdmin(admin.ModelAdmin):
    list_display = ('movimiento', 'producto', 'cantidad')
    list_filter = ('movimiento', 'producto')
    search_fields = ('producto__nombre',)

