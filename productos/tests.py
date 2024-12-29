from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .forms import ProductoForm
from .models import Autor, Editorial, Producto


class ProductoModelTest(TestCase):
    def setUp(self):
        self.editorial = Editorial.objects.create(
            nombre_editorial='Editorial Test',
            direccion='Dirección Test',
            telefono='123456789'
        )
        self.autor = Autor.objects.create(
            nombre_autor='Autor Test',
            nacionalidad='Nacionalidad Test'
        )
        self.producto = Producto.objects.create(
            nombre='Producto Test',
            tipo='libro',
            editorial=self.editorial,
            precio=Decimal('19.99')
        )
        self.producto.autores.add(self.autor)

    def test_producto_creation(self):
        self.assertTrue(isinstance(self.producto, Producto))
        self.assertEqual(str(self.producto), 'Producto Test')

    def test_producto_fields(self):
        self.assertEqual(self.producto.nombre, 'Producto Test')
        self.assertEqual(self.producto.tipo, 'libro')
        self.assertEqual(self.producto.editorial, self.editorial)
        self.assertEqual(self.producto.precio, Decimal('19.99'))
        self.assertIn(self.autor, self.producto.autores.all())

class ProductoViewsTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser', 
            email='testuser@example.com', 
            password='testpass123',
            rol='jefe_bodega'
        )
        self.client.login(username='testuser', password='testpass123')
        self.editorial = Editorial.objects.create(
            nombre_editorial='Editorial Test',
            direccion='Dirección Test',
            telefono='123456789'
        )
        self.autor = Autor.objects.create(
            nombre_autor='Autor Test',
            nacionalidad='Nacionalidad Test'
        )

    def test_lista_productos(self):
        url = reverse('lista_productos')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'productos/lista_productos.html')

    def test_crear_producto(self):
        url = reverse('crear_producto')
        data = {
            'nombre': 'Nuevo Producto',
            'tipo': 'libro',
            'editorial': self.editorial.id,
            'autores': [self.autor.id],
            'precio': '29.99'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  # Redirección después de crear
        self.assertTrue(Producto.objects.filter(nombre='Nuevo Producto').exists())

    def test_editar_producto(self):
        producto = Producto.objects.create(
            nombre='Producto Original',
            tipo='libro',
            editorial=self.editorial,
            precio=Decimal('15.99')
        )
        producto.autores.add(self.autor)
        url = reverse('editar_producto', args=[producto.id])
        data = {
            'nombre': 'Producto Editado',
            'tipo': 'revista',
            'editorial': self.editorial.id,
            'autores': [self.autor.id],
            'precio': '25.99'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  # Redirección después de editar
        producto.refresh_from_db()
        self.assertEqual(producto.nombre, 'Producto Editado')
        self.assertEqual(producto.tipo, 'revista')
        self.assertEqual(producto.precio, Decimal('25.99'))

class ProductoFormTest(TestCase):
    def setUp(self):
        self.editorial = Editorial.objects.create(
            nombre_editorial='Editorial Test',
            direccion='Dirección Test',
            telefono='123456789'
        )
        self.autor = Autor.objects.create(
            nombre_autor='Autor Test',
            nacionalidad='Nacionalidad Test'
        )

    def test_producto_form_valid(self):
        form_data = {
            'nombre': 'Producto Test',
            'tipo': 'libro',
            'editorial': self.editorial.id,
            'autores': [self.autor.id],
            'precio': '19.99'
        }
        form = ProductoForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_producto_form_invalid(self):
        form_data = {
            'nombre': '',  # Nombre vacío, debería ser inválido
            'tipo': 'libro',
            'editorial': self.editorial.id,
            'autores': [self.autor.id],
            'precio': '19.99'
        }
        form = ProductoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('nombre', form.errors)

