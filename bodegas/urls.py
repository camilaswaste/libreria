from django.urls import path

from . import views

urlpatterns = [
    path('', views.lista_bodegas, name='lista_bodegas'),
    path('crear/', views.crear_bodega, name='crear_bodega'),
    path('inventario/<int:pk>/', views.inventario_bodega, name='inventario_bodega'),
    path('agregar_producto/<int:pk>/', views.agregar_producto_bodega, name='agregar_producto_bodega'),
    path('eliminar/<int:pk>/', views.eliminar_bodega, name='eliminar_bodega'),
]

