from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AutorForm, EditorialForm, ProductoForm
from .models import Autor, Editorial, Producto


@login_required
@user_passes_test(lambda u: u.rol in ['jefe_bodega', 'admin'])
def lista_productos(request):
    query = request.GET.get('q')
    productos = Producto.objects.all().select_related('editorial').prefetch_related('autores')
    
    if query:
        productos = productos.filter(
            Q(nombre__icontains=query) |
            Q(editorial__nombre_editorial__icontains=query) |
            Q(autores__nombre_autor__icontains=query)
        ).distinct()
    
    paginator = Paginator(productos, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'productos/lista_productos.html', {'page_obj': page_obj, 'query': query})

@login_required
@user_passes_test(lambda u: u.rol in ['jefe_bodega', 'admin'])
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            producto = form.save()
            messages.success(request, 'Producto creado exitosamente')
            return redirect('lista_productos')
    else:
        form = ProductoForm()
    
    return render(request, 'productos/producto_form.html', {
        'form': form,
        'titulo': 'Crear Producto'
    })

@login_required
@user_passes_test(lambda u: u.rol in ['jefe_bodega', 'admin'])
def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado exitosamente')
            return redirect('lista_productos')
    else:
        form = ProductoForm(instance=producto)
    
    return render(request, 'productos/producto_form.html', {
        'form': form,
        'titulo': 'Editar Producto'
    })

@login_required
@user_passes_test(lambda u: u.rol in ['jefe_bodega', 'admin'])
def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        messages.success(request, 'Producto eliminado exitosamente')
        return redirect('lista_productos')
    return render(request, 'productos/confirmar_eliminar.html', {'producto': producto})

@login_required
@user_passes_test(lambda u: u.rol in ['jefe_bodega', 'admin'])
def crear_editorial(request):
    if request.method == 'POST':
        form = EditorialForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Editorial creada exitosamente')
            return redirect('lista_productos')
    else:
        form = EditorialForm()
    
    return render(request, 'productos/editorial_form.html', {
        'form': form,
        'titulo': 'Crear Editorial'
    })

@login_required
@user_passes_test(lambda u: u.rol in ['jefe_bodega', 'admin'])
def crear_autor(request):
    if request.method == 'POST':
        form = AutorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Autor creado exitosamente')
            return redirect('lista_productos')
    else:
        form = AutorForm()
    
    return render(request, 'productos/autor_form.html', {
        'form': form,
        'titulo': 'Crear Autor'
    })

@login_required
@user_passes_test(lambda u: u.rol in ['jefe_bodega', 'admin'])
def lista_autores(request):
    autores = Autor.objects.all()
    return render(request, 'productos/lista_autores.html', {'autores': autores})

@login_required
@user_passes_test(lambda u: u.rol in ['jefe_bodega', 'admin'])
def fusionar_autores(request):
    if request.method == 'POST':
        primary_id = request.POST.get('primary_author')
        duplicate_ids = request.POST.getlist('duplicate_authors')
        if primary_id and duplicate_ids:
            Autor.merge_duplicates(primary_id, duplicate_ids)
            messages.success(request, 'Autores fusionados exitosamente.')
        else:
            messages.error(request, 'Por favor, selecciona un autor principal y al menos un duplicado.')
        return redirect('lista_autores')

    duplicates = Autor.find_duplicates()
    duplicate_authors = Autor.objects.filter(nombre_autor__in=[item['nombre_autor'] for item in duplicates])
    return render(request, 'productos/fusionar_autores.html', {'duplicate_authors': duplicate_authors})

@login_required
@user_passes_test(lambda u: u.rol in ['jefe_bodega', 'admin'])
def lista_editoriales(request):
    editoriales = Editorial.objects.all()
    return render(request, 'productos/lista_editoriales.html', {'editoriales': editoriales})

@login_required
@user_passes_test(lambda u: u.rol in ['jefe_bodega', 'admin'])
def fusionar_editoriales(request):
    if request.method == 'POST':
        primary_id = request.POST.get('primary_editorial')
        duplicate_ids = request.POST.getlist('duplicate_editorials')
        if primary_id and duplicate_ids:
            Editorial.merge_duplicates(primary_id, duplicate_ids)
            messages.success(request, 'Editoriales fusionadas exitosamente.')
        else:
            messages.error(request, 'Por favor, selecciona una editorial principal y al menos una duplicada.')
        return redirect('lista_editoriales')

    duplicates = Editorial.find_duplicates()
    duplicate_editorials = Editorial.objects.filter(nombre_editorial__in=[item['nombre_editorial'] for item in duplicates])
    return render(request, 'productos/fusionar_editoriales.html', {'duplicate_editorials': duplicate_editorials})

