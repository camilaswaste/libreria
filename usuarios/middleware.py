from django.contrib import messages
from django.shortcuts import render
from django.urls import resolve


class RoleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            return self.get_response(request)

        current_url = resolve(request.path_info)
        
        role_permissions = {
            'lista_movimientos': ['bodeguero', 'jefe_bodega','admin'],
            'lista_informes': ['jefe_bodega', 'auditor','admin'],
            'lista_productos': ['jefe_bodega', 'admin'],
        }

        view_name = current_url.url_name
        if view_name in role_permissions and request.user.rol not in role_permissions[view_name]:
            messages.error(request, 'No tienes permiso para acceder a esta sección.')
            return render(request, 'usuarios/acceso_denegado.html', status=403)

        return self.get_response(request)