from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BodegaForm, BodegaProductoForm
from .models import Bodega, BodegaProducto


@login_required
def lista_bodegas(request):
    bodegas_list = Bodega.objects.all().select_related('jefe_bodega')
    paginator = Paginator(bodegas_list, 10)  
    page_number = request.GET.get('page')
    bodegas = paginator.get_page(page_number)
    return render(request, 'bodegas/lista_bodegas.html', {'bodegas': bodegas})

@login_required
@user_passes_test(lambda u: u.rol in ['jefe_bodega', 'admin'])
def crear_bodega(request):
    if request.method == 'POST':
        form = BodegaForm(request.POST)
        if form.is_valid():
            bodega = form.save()
            messages.success(request, 'Bodega creada exitosamente')
            return redirect('lista_bodegas')
    else:
        form = BodegaForm()
    
    return render(request, 'bodegas/bodega_form.html', {
        'form': form,
        'titulo': 'Crear Bodega'
    })

@login_required
def inventario_bodega(request, pk):
    bodega = get_object_or_404(Bodega, pk=pk)
    productos_list = BodegaProducto.objects.filter(bodega=bodega).select_related('producto')
    paginator = Paginator(productos_list, 20)  # Mostrar 20 productos por página
    page_number = request.GET.get('page')
    productos = paginator.get_page(page_number)
    
    return render(request, 'bodegas/inventario.html', {
        'bodega': bodega,
        'productos': productos,
        'valor_total': bodega.valor_total_inventario()
    })

@login_required
@user_passes_test(lambda u: u.rol == 'bodeguero')
def agregar_producto_bodega(request, pk):
    bodega = get_object_or_404(Bodega, pk=pk)
    
    if request.method == 'POST':
        form = BodegaProductoForm(request.POST)
        if form.is_valid():
            producto_bodega, created = BodegaProducto.objects.update_or_create(
                bodega=bodega,
                producto=form.cleaned_data['producto'],
                defaults={'cantidad': form.cleaned_data['cantidad']}
            )
            messages.success(request, 'Producto agregado o actualizado exitosamente')
            return redirect('inventario_bodega', pk=pk)
    else:
        form = BodegaProductoForm()
    
    return render(request, 'bodegas/agregar_producto.html', {
        'form': form,
        'bodega': bodega
    })

@login_required
@user_passes_test(lambda u: u.rol in ['jefe_bodega', 'admin'])
def eliminar_bodega(request, pk):
    bodega = get_object_or_404(Bodega, pk=pk)
    if request.method == 'POST':
        try:
            bodega.delete()
            messages.success(request, f'La bodega {bodega.nombre_bodega} ha sido eliminada exitosamente.')
            return redirect('lista_bodegas')
        except ProtectedError:
            messages.error(request, 'No se puede eliminar esta bodega porque tiene productos asociados.')
            return redirect('lista_bodegas')
    return render(request, 'bodegas/confirmar_eliminar_bodega.html', {'bodega': bodega})

