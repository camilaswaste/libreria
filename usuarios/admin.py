from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'rol', 'is_staff')
    list_filter = ('rol', 'is_staff', 'is_superuser', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Información adicional', {'fields': ('rol',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información adicional', {
            'classes': ('wide',),
            'fields': ('rol', 'email', 'first_name', 'last_name'),
        }),
    )
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)

