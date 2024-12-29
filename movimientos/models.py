from django.db import models, transaction
from django.utils import timezone

from bodegas.models import Bodega, BodegaProducto
from productos.models import Producto
from usuarios.models import Usuario


class Movimiento(models.Model):
    bodega_origen = models.ForeignKey(Bodega, on_delete=models.PROTECT, related_name='movimientos_origen')
    bodega_destino = models.ForeignKey(Bodega, on_delete=models.PROTECT, related_name='movimientos_destino')
    fecha_movimiento = models.DateTimeField(default=timezone.now)
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)
    productos = models.ManyToManyField(Producto, through='DetalleMovimiento')
    
    class Meta:
        db_table = 'movimientos'
        
    def __str__(self):
        fecha_local = timezone.localtime(self.fecha_movimiento)
        return f"Movimiento {self.id} - {fecha_local.strftime('%d/%m/%Y %H:%M')}"

    @transaction.atomic
    def registrar_movimiento(self):
        for detalle in self.detallemovimiento_set.all():
            stock_origen, created = BodegaProducto.objects.get_or_create(
                bodega=self.bodega_origen,
                producto=detalle.producto,
                defaults={'cantidad': 0}
            )
            if stock_origen.cantidad < detalle.cantidad:
                raise ValueError(f'Stock insuficiente para {detalle.producto} en bodega origen')
            stock_origen.cantidad -= detalle.cantidad
            stock_origen.save()

            stock_destino, created = BodegaProducto.objects.get_or_create(
                bodega=self.bodega_destino,
                producto=detalle.producto,
                defaults={'cantidad': 0}
            )
            stock_destino.cantidad += detalle.cantidad
            stock_destino.save()

class DetalleMovimiento(models.Model):
    movimiento = models.ForeignKey(Movimiento, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    
    class Meta:
        db_table = 'detalle_movimiento'

    def __str__(self):
        return f"{self.movimiento} - {self.producto}: {self.cantidad}"

