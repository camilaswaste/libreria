from django.db import models
from django.db.models import F, Sum

from productos.models import Producto
from usuarios.models import Usuario


class Bodega(models.Model):
    codigo_bodega = models.CharField(max_length=50, unique=True)
    nombre_bodega = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=255)
    jefe_bodega = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)
    productos = models.ManyToManyField(Producto, through='BodegaProducto')
    
    class Meta:
        db_table = 'bodegas'
        
    def __str__(self):
        return f"{self.codigo_bodega} - {self.nombre_bodega}"
        
    def consultar_inventario(self):
        return self.bodegaproducto_set.all()

    def valor_total_inventario(self):
        total = self.bodegaproducto_set.aggregate(
            total=Sum(F('cantidad') * F('producto__precio'))
        )['total']
        return total if total is not None else 0

class BodegaProducto(models.Model):
    bodega = models.ForeignKey(Bodega, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    
    class Meta:
        db_table = 'bodega_productos'
        unique_together = ('bodega', 'producto')

    def __str__(self):
        return f"{self.bodega.nombre_bodega} - {self.producto.nombre}: {self.cantidad}"

