import csv
import os

from django.conf import settings
from django.db import models
from django.utils import timezone

from bodegas.models import BodegaProducto
from movimientos.models import Movimiento
from usuarios.models import Usuario


class Informe(models.Model):
    TIPOS = (
        ('movimientos', 'Informe de Movimientos'),
        ('inventario', 'Informe de Inventario'),
    )
    
    usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT)
    tipo_informe = models.CharField(max_length=20, choices=TIPOS)
    fecha_generacion = models.DateTimeField(default=timezone.now)
    nombre_archivo = models.CharField(max_length=255, null=True, blank=True)
    
    class Meta:
        db_table = 'informes'
        
    def __str__(self):
        return f"{self.get_tipo_informe_display()} - {self.fecha_generacion}"
    
    def generar_informe(self):
        # Asegurar que el directorio de informes exista
        directorio_informes = os.path.join(settings.BASE_DIR, 'informes')
        if not os.path.exists(directorio_informes):
            os.makedirs(directorio_informes)
            
        if self.tipo_informe == 'movimientos':
            return self.generar_informe_movimiento()
        elif self.tipo_informe == 'inventario':
            return self.generar_informe_inventario()
    
    def generar_informe_movimiento(self):
        fecha_actual = timezone.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"informe_movimientos_{fecha_actual}.csv"
        ruta_archivo = os.path.join(settings.BASE_DIR, 'informes', nombre_archivo)
        
        with open(ruta_archivo, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Fecha", "Bodega Origen", "Bodega Destino", "Producto", "Cantidad"])
            
            movimientos = Movimiento.objects.all().select_related('bodega_origen', 'bodega_destino').prefetch_related('detallemovimiento_set__producto')
            for movimiento in movimientos:
                for detalle in movimiento.detallemovimiento_set.all():
                    writer.writerow([
                        movimiento.fecha_movimiento,
                        movimiento.bodega_origen.nombre_bodega,
                        movimiento.bodega_destino.nombre_bodega,
                        detalle.producto.nombre,
                        detalle.cantidad
                    ])
        
        self.nombre_archivo = nombre_archivo
        self.save()
        return ruta_archivo
        
    def generar_informe_inventario(self):
        fecha_actual = timezone.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"informe_inventario_{fecha_actual}.csv"
        ruta_archivo = os.path.join(settings.BASE_DIR, 'informes', nombre_archivo)
        
        with open(ruta_archivo, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Bodega", "Producto", "Cantidad"])
            
            inventario = BodegaProducto.objects.all().select_related('bodega', 'producto')
            for item in inventario:
                writer.writerow([
                    item.bodega.nombre_bodega,
                    item.producto.nombre,
                    item.cantidad
                ])
        
        self.nombre_archivo = nombre_archivo
        self.save()
        return ruta_archivo

