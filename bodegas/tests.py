from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from productos.models import Producto

from .models import Bodega, BodegaProducto


class BodegaModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='jefebodega',
            email='jefe@example.com',
            password='testpass123',
            rol='jefe_bodega'
        )
        self.bodega = Bodega.objects.create(
            codigo_bodega='BOD001',
            nombre_bodega='Bodega Test',
            ubicacion='Ubicación Test',
            jefe_bodega=self.user
        )
        self.producto = Producto.objects.create(
            nombre='Producto Test',
            tipo='libro',
            precio=19.99
        )
        self.bodega_producto = BodegaProducto.objects.create(
            bodega=self.bodega,
            producto=self.producto,
            cantidad=10
        )

    def test_bodega_creation(self):
        self.assertTrue(isinstance(self.bodega, Bodega))
        self.assertEqual(str(self.bodega), 'BOD001 - Bodega Test')

    def test_bodega_producto_creation(self):
        self.assertTrue(isinstance(self.bodega_producto, BodegaProducto))
        self.assertEqual(str(self.bodega_producto), 'Bodega Test - Producto Test: 10')

    def test_consultar_inventario(self):
        inventario = self.bodega.consultar_inventario()
        self.assertEqual(inventario.count(), 1)
        self.assertEqual(inventario.first(), self.bodega_producto)

    def test_valor_total_inventario(self):
        valor_total = self.bodega.valor_total_inventario()
        self.assertEqual(valor_total, 199.90)  # 10 * 19.99

class BodegaViewsTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser', 
            email='testuser@example.com', 
            password='testpass123',
            rol='jefe_bodega'
        )
        self.client.login(username='testuser', password='testpass123')
        self.bodega = Bodega.objects.create(
            codigo_bodega='BOD001',
            nombre_bodega='Bodega Test',
            ubicacion='Ubicación Test',
            jefe_bodega=self.user
        )

    def test_lista_bodegas(self):
        url = reverse('lista_bodegas')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bodegas/lista_bodegas.html')

    def test_crear_bodega(self):
        url = reverse('crear_bodega')
        data = {
            'codigo_bodega': 'BOD002',
            'nombre_bodega': 'Nueva Bodega',
            'ubicacion': 'Nueva Ubicación',
            'jefe_bodega': self.user.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  
        self.assertTrue(Bodega.objects.filter(codigo_bodega='BOD002').exists())

    def test_inventario_bodega(self):
        url = reverse('inventario_bodega', args=[self.bodega.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bodegas/inventario.html')

    def test_agregar_producto_bodega(self):
        producto = Producto.objects.create(
            nombre='Nuevo Producto',
            tipo='libro',
            precio=29.99
        )
        url = reverse('agregar_producto_bodega', args=[self.bodega.id])
        data = {
            'producto': producto.id,
            'cantidad': 5
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  
        self.assertTrue(BodegaProducto.objects.filter(bodega=self.bodega, producto=producto).exists())

