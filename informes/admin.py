from django.contrib import admin

from .models import Informe


@admin.register(Informe)
class InformeAdmin(admin.ModelAdmin):
    list_display = ('tipo_informe', 'usuario', 'fecha_generacion', 'nombre_archivo')
    list_filter = ('tipo_informe', 'fecha_generacion')
    search_fields = ('usuario__username', 'tipo_informe')
    readonly_fields = ('fecha_generacion',)

