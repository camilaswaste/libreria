from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from movimientos.models import Movimiento

from .forms import EditarPerfilForm, RegistroForm, UsuarioForm
from .models import Usuario


def home(request):
    return render(request, 'usuarios/home.html')

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registro exitoso. Bienvenido!')
            return redirect('home')
    else:
        form = RegistroForm()
    return render(request, 'usuarios/registro.html', {'form': form})

def iniciar_sesion(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', reverse('home'))
            return redirect(next_url)
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    return render(request, 'usuarios/login.html')

@login_required
def perfil(request):
    return render(request, 'usuarios/perfil.html')

@login_required
def editar_perfil(request):
    if request.method == 'POST':
        form = EditarPerfilForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado exitosamente')
            return redirect('perfil')
    else:
        form = EditarPerfilForm(instance=request.user)
    return render(request, 'usuarios/editar_perfil.html', {'form': form})

@user_passes_test(lambda u: u.rol == 'admin')
def lista_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'usuarios/lista_usuarios.html', {'usuarios': usuarios})

@user_passes_test(lambda u: u.rol == 'admin')
def crear_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario creado exitosamente.')
            return redirect('lista_usuarios')
    else:
        form = UsuarioForm()
    return render(request, 'usuarios/usuario_form.html', {'form': form, 'titulo': 'Crear Usuario'})

@user_passes_test(lambda u: u.rol == 'admin')
def editar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario actualizado exitosamente.')
            return redirect('lista_usuarios')
    else:
        form = UsuarioForm(instance=usuario)
    return render(request, 'usuarios/usuario_form.html', {'form': form, 'titulo': 'Editar Usuario'})

@user_passes_test(lambda u: u.rol == 'admin')
def eliminar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        try:
            movimientos = Movimiento.objects.filter(usuario=usuario)
            if movimientos.exists():
                movimientos.update(usuario=None)
                messages.warning(request, f'Se han desvinculado {movimientos.count()} movimientos del usuario.')
            
            usuario.delete()
            messages.success(request, 'Usuario eliminado exitosamente.')
            return redirect('lista_usuarios')
        except Exception as e:
            messages.error(request, f'Error al eliminar el usuario: {str(e)}')
            return redirect('lista_usuarios')
    
    return render(request, 'usuarios/confirmar_eliminar_usuario.html', {'usuario': usuario})

def cerrar_sesion(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión exitosamente.')
    return redirect('home')

