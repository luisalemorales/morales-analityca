import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'psycho_project.settings')
django.setup()

from dashboard.models import Cliente

def seed():
    print("Iniciando la precarga de datos psicográficos de prueba...")
    
    # Limpiar clientes existentes para evitar duplicados en la demo
    Cliente.objects.all().delete()
    print("Base de datos limpia.")

    clientes_demo = [
        {
            'nombre': 'Alejandro Sanz',
            'empresa': 'Música & Media Corp',
            'telefono': '+34 622 111 222',
            'direccion': 'Paseo de la Castellana 45, Madrid, España',
            'latitud': 40.43813,
            'longitud': -3.68962,
            'ocean_o': 85,
            'ocean_c': 40,
            'ocean_e': 90,
            'ocean_a': 75,
            'ocean_n': 35,
            'intereses': 'Arte, Espectáculos, Nuevas Tendencias, Filantropía'
        },
        {
            'nombre': 'Claudia Sheinbaum',
            'empresa': 'Gobierno CDMX',
            'telefono': '+52 55 1234 5678',
            'direccion': 'Plaza de la Constitución S/N, Centro Histórico, CDMX, México',
            'latitud': 19.43260,
            'longitud': -99.13320,
            'ocean_o': 65,
            'ocean_c': 90,
            'ocean_e': 50,
            'ocean_a': 60,
            'ocean_n': 40,
            'intereses': 'Política Pública, Ciencias Ambientales, Planificación Estratégica'
        },
        {
            'nombre': 'Carlos Vives',
            'empresa': 'Cultura & Ritmo S.A.S',
            'telefono': '+57 300 987 6543',
            'direccion': 'Parque de la 93, Bogotá, Colombia',
            'latitud': 4.67680,
            'longitud': -74.04830,
            'ocean_o': 80,
            'ocean_c': 45,
            'ocean_e': 85,
            'ocean_a': 80,
            'ocean_n': 30,
            'intereses': 'Música Tradicional, Desarrollo Sostenible, Gastronomía'
        },
        {
            'nombre': 'Marta Ortega',
            'empresa': 'Inditex Group',
            'telefono': '+34 981 180 000',
            'direccion': 'Avenida de la Diputación S/N, Arteixo, A Coruña, España',
            'latitud': 43.30420,
            'longitud': -8.50470,
            'ocean_o': 70,
            'ocean_c': 85,
            'ocean_e': 60,
            'ocean_a': 55,
            'ocean_n': 45,
            'intereses': 'Moda de Vanguardia, Liderazgo Corporativo, Equitación'
        },
        {
            'nombre': 'Andrés Cepeda',
            'empresa': 'Canto Bogotá Producciones',
            'telefono': '+57 311 222 3333',
            'direccion': 'Usaquén Plaza, Bogotá, Colombia',
            'latitud': 4.70110,
            'longitud': -74.03050,
            'ocean_o': 75,
            'ocean_c': 60,
            'ocean_e': 70,
            'ocean_a': 85,
            'ocean_n': 40,
            'intereses': 'Producción Musical, Restaurantes, Educación Infantil'
        },
        {
            'nombre': 'Ing. Roberto Gómez',
            'empresa': 'Tech Solutions Latam',
            'telefono': '+52 55 9988 7766',
            'direccion': 'Paseo de la Reforma, CDMX, México',
            'latitud': 19.42700,
            'longitud': -99.16760,
            'ocean_o': 55,
            'ocean_c': 75,
            'ocean_e': 40,
            'ocean_a': 65,
            'ocean_n': 75,
            'intereses': 'Ciberseguridad, Blockchain, Automatización de Procesos'
        }
    ]

    for data in clientes_demo:
        cliente = Cliente(**data)
        cliente.save()
        print(f"Registrado: {cliente.nombre} | Comportamiento: {cliente.comportamiento_compra} | Estilo Decisión: {cliente.estilo_decision}")

    print("Precarga finalizada con éxito. 6 clientes demos inyectados en SQLite3.")

if __name__ == '__main__':
    seed()
