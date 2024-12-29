from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from bodegas.models import Bodega, BodegaProducto
from productos.models import Producto

from .models import DetalleMovimiento, Movimiento


class MovimientoModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            rol='bodeguero'
        )
        self.bodega_origen = Bodega.objects.create(
            codigo_bodega='BOD001',
            nombre_bodega='Bodega Origen',
            ubicacion='Ubicación A'
        )
        self.bodega_destino = Bodega.objects.create(
            codigo_bodega='BOD002',
            nombre_bodega='Bodega Destino',
            ubicacion='Ubicación B'
        )
        self.producto = Producto.objects.create(
            nombre='Producto Test',
            tipo='libro',
            precio=100
        )
        self.movimiento = Movimiento.objects.create(
            bodega_origen=self.bodega_origen,
            bodega_destino=self.bodega_destino,
            usuario=self.user
        )
        self.detalle_movimiento = DetalleMovimiento.objects.create(
            movimiento=self.movimiento,
            producto=self.producto,
            cantidad=5
        )

    def test_movimiento_creation(self):
        self.assertTrue(isinstance(self.movimiento, Movimiento))
        self.assertEqual(self.movimiento.bodega_origen, self.bodega_origen)
        self.assertEqual(self.movimiento.bodega_destino, self.bodega_destino)
        self.assertEqual(self.movimiento.usuario, self.user)

    def test_detalle_movimiento_creation(self):
        self.assertTrue(isinstance(self.detalle_movimiento, DetalleMovimiento))
        self.assertEqual(self.detalle_movimiento.movimiento, self.movimiento)
        self.assertEqual(self.detalle_movimiento.producto, self.producto)
        self.assertEqual(self.detalle_movimiento.cantidad, 5)

class MovimientoViewsTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser', 
            email='testuser@example.com', 
            password='testpass123',
            rol='bodeguero'
        )
        self.client.login(username='testuser', password='testpass123')
        self.bodega_origen = Bodega.objects.create(
            codigo_bodega='BOD001',
            nombre_bodega='Bodega Origen',
            ubicacion='Ubicación A'
        )
        self.bodega_destino = Bodega.objects.create(
            codigo_bodega='BOD002',
            nombre_bodega='Bodega Destino',
            ubicacion='Ubicación B'
        )
        self.producto = Producto.objects.create(
            nombre='Producto Test',
            tipo='libro',
            precio=100
        )
        BodegaProducto.objects.create(
            bodega=self.bodega_origen,
            producto=self.producto,
            cantidad=50
        )

    def test_lista_movimientos(self):
        url = reverse('lista_movimientos')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'movimientos/lista_movimientos.html')

    def test_crear_movimiento(self):
        url = reverse('crear_movimiento')
        data = {
            'bodega_origen': self.bodega_origen.id,
            'bodega_destino': self.bodega_destino.id,
            'detallemovimiento_set-TOTAL_FORMS': '1',
            'detallemovimiento_set-INITIAL_FORMS': '0',
            'detallemovimiento_set-0-producto': self.producto.id,
            'detallemovimiento_set-0-cantidad': 10,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  
        self.assertTrue(Movimiento.objects.exists())
        
        # Verificar que el inventario se actualizó correctamente
        inventario_origen = BodegaProducto.objects.get(bodega=self.bodega_origen, producto=self.producto)
        inventario_destino = BodegaProducto.objects.get(bodega=self.bodega_destino, producto=self.producto)
        self.assertEqual(inventario_origen.cantidad, 40)  # 50 - 10
        self.assertEqual(inventario_destino.cantidad, 10)

    def test_detalle_movimiento(self):
        movimiento = Movimiento.objects.create(
            bodega_origen=self.bodega_origen,
            bodega_destino=self.bodega_destino,
            usuario=self.user
        )
        DetalleMovimiento.objects.create(
            movimiento=movimiento,
            producto=self.producto,
            cantidad=5
        )
        url = reverse('detalle_movimiento', args=[movimiento.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'movimientos/detalle_movimiento.html')

class MovimientoIntegrationTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='bodeguero',
            password='testpass123',
            rol='bodeguero'
        )
        self.bodega_origen = Bodega.objects.create(
            codigo_bodega='BOD001',
            nombre_bodega='Bodega Origen',
            ubicacion='Ubicación A'
        )
        self.bodega_destino = Bodega.objects.create(
            codigo_bodega='BOD002',
            nombre_bodega='Bodega Destino',
            ubicacion='Ubicación B'
        )
        self.producto = Producto.objects.create(
            nombre='Producto Test',
            tipo='libro',
            precio=100
        )
        BodegaProducto.objects.create(
            bodega=self.bodega_origen,
            producto=self.producto,
            cantidad=50
        )
        self.client.login(username='bodeguero', password='testpass123')

    def test_crear_movimiento_y_actualizar_inventario(self):
        url = reverse('crear_movimiento')
        data = {
            'bodega_origen': self.bodega_origen.id,
            'bodega_destino': self.bodega_destino.id,
            'detallemovimiento_set-TOTAL_FORMS': '1',
            'detallemovimiento_set-INITIAL_FORMS': '0',
            'detallemovimiento_set-0-producto': self.producto.id,
            'detallemovimiento_set-0-cantidad': 10,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302) 

        # Verificar que el movimiento se creó
        self.assertTrue(Movimiento.objects.exists())
        movimiento = Movimiento.objects.first()
        self.assertEqual(movimiento.bodega_origen, self.bodega_origen)
        self.assertEqual(movimiento.bodega_destino, self.bodega_destino)

        # Verificar que el inventario se actualizó correctamente
        inventario_origen = BodegaProducto.objects.get(bodega=self.bodega_origen, producto=self.producto)
        inventario_destino = BodegaProducto.objects.get(bodega=self.bodega_destino, producto=self.producto)
        self.assertEqual(inventario_origen.cantidad, 40)  # 50 - 10
        self.assertEqual(inventario_destino.cantidad, 10)

    def test_movimiento_con_stock_insuficiente(self):
        url = reverse('crear_movimiento')
        data = {
            'bodega_origen': self.bodega_origen.id,
            'bodega_destino': self.bodega_destino.id,
            'detallemovimiento_set-TOTAL_FORMS': '1',
            'detallemovimiento_set-INITIAL_FORMS': '0',
            'detallemovimiento_set-0-producto': self.producto.id,
            'detallemovimiento_set-0-cantidad': 60,  # Más que el stock disponible
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)  # Se queda en la misma página

        # Verificar que no se creó el movimiento
        self.assertFalse(Movimiento.objects.exists())

        # Verificar que el inventario no cambió
        inventario_origen = BodegaProducto.objects.get(bodega=self.bodega_origen, producto=self.producto)
        self.assertEqual(inventario_origen.cantidad, 50)

