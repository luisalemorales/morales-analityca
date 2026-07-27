from django.urls import path
from . import views

# IMPORTANTE: Si esta línea existe en tu archivo, tenlo en cuenta para el paso 2
# app_name = 'dashboard' 

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    
    # Esta línea resuelve tu error NoReverseMatch:
    path('registrar-cliente/', views.registrar_cliente, name='registrar_cliente'),
    
    # Asegúrate de tener también las demás rutas que usa tu plantilla:
    path('api/clientes/', views.api_clientes, name='api_clientes'),
    path('exportar-excel/', views.exportar_excel, name='exportar_excel'),
    path('importar-excel/', views.importar_excel, name='importar_excel'),
    path('eliminar-masivo/', views.eliminar_masivo, name='eliminar_masivo'),
]
