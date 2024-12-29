import logging
import os

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .models import Informe

logger = logging.getLogger(__name__)

def check_informes_permission(user):
    return user.rol in ['admin', 'jefe_bodega', 'auditor']

def check_generar_informes_permission(user):
    return user.rol in ['admin', 'auditor']

@login_required
@user_passes_test(check_informes_permission)
def lista_informes(request):
    logger.debug(f"User {request.user.username} (role: {request.user.rol}) accessed lista_informes")
    informes_list = Informe.objects.all().select_related('usuario')
    paginator = Paginator(informes_list, 10)
    page_number = request.GET.get('page')
    informes = paginator.get_page(page_number)
    return render(request, 'informes/lista_informes.html', {'informes': informes})

@login_required
@user_passes_test(check_generar_informes_permission)
def generar_informe(request, tipo_informe):
    if tipo_informe not in dict(Informe.TIPOS):
        messages.error(request, 'Tipo de informe no válido')
        return redirect('lista_informes')
    
    informe = Informe.objects.create(
        usuario=request.user,
        tipo_informe=tipo_informe
    )
    
    try:
        ruta_archivo = informe.generar_informe()
        messages.success(request, 'Informe generado exitosamente')
    except Exception as e:
        logger.error(f"Error generando informe: {str(e)}")
        informe.delete()
        messages.error(request, f'Error al generar el informe: {str(e)}')
    
    return redirect('lista_informes')

@login_required
@user_passes_test(check_informes_permission)
def descargar_informe(request, informe_id):
    informe = get_object_or_404(Informe, pk=informe_id)
    
    ruta_archivo = os.path.join(settings.BASE_DIR, 'informes', informe.nombre_archivo)
    
    try:
        with open(ruta_archivo, 'rb') as archivo:
            response = HttpResponse(archivo.read(), content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = f'attachment; filename="{informe.nombre_archivo}"'
            return response
    except FileNotFoundError:
        logger.error(f"Archivo no encontrado: {ruta_archivo}")
        messages.error(request, 'El archivo del informe no se encuentra disponible.')
        return redirect('lista_informes')
    except Exception as e:
        logger.error(f"Error al descargar informe: {str(e)}")
        messages.error(request, 'Error al descargar el informe.')
        return redirect('lista_informes')

@login_required
@user_passes_test(check_generar_informes_permission)
def eliminar_informe(request, informe_id):
    informe = get_object_or_404(Informe, pk=informe_id)
    
    if request.method == 'POST':
        try:
            # Eliminar el archivo físico
            ruta_archivo = os.path.join(settings.BASE_DIR, 'informes', informe.nombre_archivo)
            if os.path.exists(ruta_archivo):
                os.remove(ruta_archivo)
            
            # Eliminar el registro de la base de datos
            informe.delete()
            messages.success(request, 'Informe eliminado exitosamente.')
        except Exception as e:
            logger.error(f"Error al eliminar informe: {str(e)}")
            messages.error(request, 'Error al eliminar el informe.')
        
        return redirect('lista_informes')
    
    # Si es una solicitud GET, mostrar página de confirmación
    return render(request, 'informes/confirmar_eliminar.html', {'informe': informe})