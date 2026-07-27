from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Endpoints de API para Clientes
    path('api/clientes/', views.api_clientes, name='api_clientes'),
    path('api/clientes/crear/', views.crear_cliente, name='crear_cliente'),
    path('api/clientes/eliminar/', views.eliminar_clientes, name='eliminar_clientes'),
    
    # Módulo de Importación y Exportación de Excel
    path('exportar-excel/', views.exportar_excel, name='exportar_excel'),
    path('importar-excel/', views.importar_excel, name='importar_excel'),
]
