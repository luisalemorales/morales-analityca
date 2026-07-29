from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('api/clientes/', views.api_clientes, name='api_clientes'),
    path('api/clientes/delete/', views.eliminar_clientes, name='eliminar_clientes'),
    path('export/', views.exportar_excel, name='exportar_excel'),
    path('import/', views.importar_excel, name='importar_excel'),
]
