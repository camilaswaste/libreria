from django.urls import path

from . import views

urlpatterns = [
    path('', views.lista_movimientos, name='lista_movimientos'),
    path('crear/', views.crear_movimiento, name='crear_movimiento'),
    path('detalle/<int:pk>/', views.detalle_movimiento, name='detalle_movimiento'),
]

