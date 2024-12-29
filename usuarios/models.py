from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    ROLES = (
        ('admin', 'Administrador'),
        ('jefe_bodega', 'Jefe de Bodega'),
        ('bodeguero', 'Bodeguero'),
        ('auditor', 'Auditor'),
    )
    rol = models.CharField(max_length=20, choices=ROLES)

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name='usuario_set',
        related_query_name='usuario',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='usuario_set',
        related_query_name='usuario',
    )

    class Meta:
        db_table = 'usuarios'
        
    def obtener_rol(self):
        return self.rol
        
    def validar_credenciales(self, nombre_usuario, contraseña):
        return self.username == nombre_usuario and self.check_password(contraseña)

