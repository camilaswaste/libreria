from django.contrib import admin

from .models import Autor, Editorial, Producto


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'editorial', 'precio')
    list_filter = ('tipo', 'editorial')
    search_fields = ('nombre', 'editorial__nombre_editorial')
    filter_horizontal = ('autores',)

@admin.register(Editorial)
class EditorialAdmin(admin.ModelAdmin):
    list_display = ('nombre_editorial', 'direccion', 'telefono')
    search_fields = ('nombre_editorial',)

@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ('nombre_autor', 'nacionalidad')
    search_fields = ('nombre_autor',)


