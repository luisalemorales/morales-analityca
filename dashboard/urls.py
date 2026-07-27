from django.urls import path
from . import views

urlpatterns = [
    # Autenticación
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Vista principal
    path('', views.dashboard_view, name='dashboard'),
    
    # API endpoints
    path('api/clientes/', views.api_clientes, name='api_clientes'),
    path('registrar-cliente/', views.registrar_cliente, name='registrar_cliente'),
    path('crear-cliente/', views.crear_cliente, name='crear_cliente'),
    
    # Import / Export
    path('exportar-excel/', views.exportar_excel, name='exportar_excel'),
    path('importar-excel/', views.importar_excel, name='importar_excel'),
    
    # Eliminación
    path('eliminar-clientes/', views.eliminar_clientes, name='eliminar_clientes'),
    path('eliminar-masivo/', views.eliminar_clientes, name='eliminar_masivo'),
]
