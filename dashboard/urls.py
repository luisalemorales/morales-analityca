from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('registrar-cliente/', views.registrar_cliente, name='registrar_cliente'),
]
