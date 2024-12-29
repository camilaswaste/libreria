import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from bodegas.models import BodegaProducto

from .forms import DetalleMovimientoFormSet, MovimientoForm
from .models import DetalleMovimiento, Movimiento

logger = logging.getLogger(__name__)

@login_required
@user_passes_test(lambda u: u.rol in ['bodeguero', 'jefe_bodega', 'admin'])
def lista_movimientos(request):
    movimientos_list = Movimiento.objects.all().select_related(
        'bodega_origen', 'bodega_destino', 'usuario'
    ).prefetch_related('productos').order_by('-fecha_movimiento')
    
    paginator = Paginator(movimientos_list, 10)
    page_number = request.GET.get('page')
    movimientos = paginator.get_page(page_number)
    return render(request, 'movimientos/lista_movimientos.html', {'movimientos': movimientos})

@login_required
@user_passes_test(lambda u: u.rol in ['bodeguero', 'jefe_bodega', 'admin'])
def crear_movimiento(request):
    if request.method == 'POST':
        form = MovimientoForm(request.POST)
        formset = DetalleMovimientoFormSet(request.POST)
        
        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    movimiento = form.save(commit=False)
                    movimiento.usuario = request.user
                    movimiento.save()
                    
                    formset.instance = movimiento
                    formset.save()
                    
                    movimiento.registrar_movimiento()
                    
                    messages.success(request, 'Movimiento registrado exitosamente')
                    return redirect('lista_movimientos')
            except ValueError as e:
                messages.error(request, str(e))
            except Exception as e:
                messages.error(request, f'Error al registrar movimiento: {str(e)}')
    else:
        form = MovimientoForm()
        formset = DetalleMovimientoFormSet()
    
    return render(request, 'movimientos/movimiento_form.html', {
        'form': form,
        'formset': formset
    })

@login_required
@user_passes_test(lambda u: u.rol in ['bodeguero', 'jefe_bodega', 'admin'])
def detalle_movimiento(request, pk):
    logger.debug(f"Accediendo a detalle_movimiento con pk={pk}")
    try:
        movimiento = get_object_or_404(Movimiento, pk=pk)
        logger.debug(f"Movimiento encontrado: {movimiento}")
        detalles = DetalleMovimiento.objects.filter(movimiento=movimiento).select_related('producto')
        logger.debug(f"Detalles encontrados: {detalles.count()}")
        context = {'movimiento': movimiento, 'detalles': detalles}
        logger.debug(f"Renderizando template con contexto: {context}")
        return render(request, 'movimientos/detalle_movimiento.html', context)
    except Exception as e:
        logger.exception(f"Error en detalle_movimiento: {str(e)}")
        messages.error(request, f"Error al cargar los detalles del movimiento: {str(e)}")
        return redirect('lista_movimientos')

