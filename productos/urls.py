from django.urls import path

from . import views

urlpatterns = [
    path('', views.lista_productos, name='lista_productos'),
    path('crear/', views.crear_producto, name='crear_producto'),
    path('editar/<int:pk>/', views.editar_producto, name='editar_producto'),
    path('eliminar/<int:pk>/', views.eliminar_producto, name='eliminar_producto'),
    path('editorial/crear/', views.crear_editorial, name='crear_editorial'),
    path('autor/crear/', views.crear_autor, name='crear_autor'),
    path('autores/', views.lista_autores, name='lista_autores'),
    path('autores/fusionar/', views.fusionar_autores, name='fusionar_autores'),
    path('editoriales/', views.lista_editoriales, name='lista_editoriales'),
    path('editoriales/fusionar/', views.fusionar_editoriales, name='fusionar_editoriales'),
]

