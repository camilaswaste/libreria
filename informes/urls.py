from django.urls import path

from . import views

urlpatterns = [
    path('', views.lista_informes, name='lista_informes'),
    path('generar/<str:tipo_informe>/', views.generar_informe, name='generar_informe'),
    path('descargar/<int:informe_id>/', views.descargar_informe, name='descargar_informe'),
    path('eliminar/<int:informe_id>/', views.eliminar_informe, name='eliminar_informe'),
]

