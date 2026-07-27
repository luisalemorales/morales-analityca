from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('registrar-cliente/', views.registrar_cliente, name='registrar_cliente'),
    
    # Rutas para la importación y exportación a Excel:
    path('exportar-excel/', views.exportar_excel, name='exportar_excel'),
    path('importar-excel/', views.importar_excel, name='importar_excel'),
]
