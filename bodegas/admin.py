from django.contrib import admin

from .models import Bodega, BodegaProducto


class BodegaProductoInline(admin.TabularInline):
    model = BodegaProducto
    extra = 1

@admin.register(Bodega)
class BodegaAdmin(admin.ModelAdmin):
    list_display = ('codigo_bodega', 'nombre_bodega', 'ubicacion', 'jefe_bodega')
    search_fields = ('codigo_bodega', 'nombre_bodega')
    inlines = [BodegaProductoInline]

@admin.register(BodegaProducto)
class BodegaProductoAdmin(admin.ModelAdmin):
    list_display = ('bodega', 'producto', 'cantidad')
    list_filter = ('bodega',)
    search_fields = ('bodega__nombre_bodega', 'producto__nombre')

