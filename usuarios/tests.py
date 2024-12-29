from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from .models import Usuario


class UsuarioModelTest(TestCase):
    def setUp(self):
        self.usuario_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'securepassword123',
            'rol': 'bodeguero'
        }
        self.usuario = Usuario.objects.create_user(**self.usuario_data)

    def test_usuario_creation(self):
        self.assertTrue(isinstance(self.usuario, Usuario))
        self.assertEqual(self.usuario.__str__(), self.usuario.username)

    def test_usuario_fields(self):
        self.assertEqual(self.usuario.email, 'test@example.com')
        self.assertEqual(self.usuario.rol, 'bodeguero')
        self.assertTrue(self.usuario.check_password('securepassword123'))

    def test_usuario_roles(self):
        valid_roles = ['admin', 'jefe_bodega', 'bodeguero', 'auditor']
        for role in valid_roles:
            self.usuario.rol = role
            self.usuario.full_clean()  

        self.usuario.rol = 'invalid_role'
        with self.assertRaises(ValidationError):
            self.usuario.full_clean()

class UsuarioViewsTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser', 
            email='testuser@example.com', 
            password='testpass123',
            rol='bodeguero'
        )
        self.client.login(username='testuser', password='testpass123')

    def test_perfil_view(self):
        response = self.client.get(reverse('perfil'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'usuarios/perfil.html')

    def test_editar_perfil_view(self):
        response = self.client.get(reverse('editar_perfil'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'usuarios/editar_perfil.html')

        data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'newemail@example.com'
        }
        response = self.client.post(reverse('editar_perfil'), data)
        self.assertEqual(response.status_code, 302) 
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'newemail@example.com')

class SecurityTest(TestCase):
    def setUp(self):
        self.admin = get_user_model().objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123',
            rol='admin'
        )
        self.bodeguero = get_user_model().objects.create_user(
            username='bodeguero',
            email='bodeguero@example.com',
            password='bodegueropass123',
            rol='bodeguero'
        )

    def test_unauthorized_access(self):
        # Prueba de acceso a la página de administración sin iniciar sesión
        response = self.client.get(reverse('admin:index'))
        self.assertEqual(response.status_code, 302)  

        # Prueba de acceso a crear página de producto como bodeguero (no autorizado)
        self.client.login(username='bodeguero', password='bodegueropass123')
        response = self.client.get(reverse('crear_producto'))
        self.assertEqual(response.status_code, 403)  # Forbidden

    def test_authorized_access(self):
        # Prueba de acceso a la página de administración como administrador
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get(reverse('admin:index'))
        self.assertEqual(response.status_code, 200)

        # Prueba de acceso a página de creación de movimiento como bodeguero (autorizado)
        self.client.login(username='bodeguero', password='bodegueropass123')
        response = self.client.get(reverse('crear_movimiento'))
        self.assertEqual(response.status_code, 200)

    def test_password_storage(self):
        # Verificar que las contraseñas no estén almacenadas en texto plano
        user = get_user_model().objects.get(username='admin')
        self.assertNotEqual(user.password, 'adminpass123')
        self.assertTrue(user.check_password('adminpass123'))

