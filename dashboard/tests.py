from django.test import TestCase, Client as HttpClient
from django.urls import reverse
from django.contrib.auth.models import User
from dashboard.models import Cliente
import pandas as pd
import io

class PsychographicAppTests(TestCase):
    def setUp(self):
        # Create default operator user
        self.username = "operator_test"
        self.password = "security_key_test_123"
        self.user = User.objects.create_user(
            username=self.username,
            email="test@ciberintelligence.gov",
            password=self.password
        )
        
        # Create a sample client target
        self.client_node = Cliente.objects.create(
            nombre="Agente K",
            empresa="MIB",
            telefono="+1 555 999 888",
            direccion="Times Square, NY",
            latitud=40.7580,
            longitud=-73.9855,
            ocean_o=90,
            ocean_c=80,
            ocean_e=70,
            ocean_a=60,
            ocean_n=30,
            intereses="Extraterrestres, Neutralizadores, Trajes Negros"
        )
        
        self.client = HttpClient()

    def test_unauthenticated_redirection(self):
        """Verify that accessing dashboard pages without authentication redirects to login."""
        protected_urls = [
            reverse('dashboard'),
            reverse('api_clientes'),
            reverse('exportar_excel'),
            reverse('importar_excel')
        ]
        
        for url in protected_urls:
            response = self.client.get(url)
            # Should redirect or return 302 to login page
            self.assertEqual(response.status_code, 302)
            self.assertIn(reverse('login'), response.url)

    def test_successful_login(self):
        """Verify that operator can log in successfully with valid credentials."""
        response = self.client.post(reverse('login'), {
            'username': self.username,
            'password': self.password
        })
        # Should redirect to dashboard
        self.assertRedirects(response, reverse('dashboard'))

    def test_dashboard_view_authenticated(self):
        """Verify that dashboard renders metrics when authenticated."""
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/dashboard.html')
        self.assertContains(response, "RED DE MAPEO PSICOGRÁFICO")

    def test_api_clients_get(self):
        """Verify that authenticated operator can retrieve clients list as JSON."""
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('api_clientes'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'success')
        self.assertTrue(len(data['data']) > 0)
        self.assertEqual(data['data'][0]['nombre'], "Agente K")

    def test_api_clients_post(self):
        """Verify that API allows injecting new clients and auto-calculates predictions."""
        self.client.login(username=self.username, password=self.password)
        new_client_data = {
            'nombre': 'Edward Snowden',
            'empresa': 'NSA whistleblower',
            'telefono': '+7 900 123 456',
            'direccion': 'Moscow, Russia',
            'latitud': 55.7558,
            'longitud': 37.6173,
            'ocean_o': 95,
            'ocean_c': 90,
            'ocean_e': 40,
            'ocean_a': 70,
            'ocean_n': 60,
            'intereses': 'Criptografía, Privacidad, Espionaje'
        }
        
        response = self.client.post(
            reverse('api_clientes'), 
            data=new_client_data
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'success')
        
        # Verify database save
        db_client = Cliente.objects.get(nombre='Edward Snowden')
        self.assertEqual(db_client.latitud, 55.7558)
        # Verify OCEAN logic triggers were called and saved
        self.assertIsNotNone(db_client.comportamiento_compra)
        self.assertIsNotNone(db_client.estilo_decision)
        self.assertIsNotNone(db_client.disparadores_compra)

    def test_export_excel(self):
        """Verify that export endpoint returns a valid spreadsheet file download."""
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('exportar_excel'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        self.assertTrue(response.has_header('Content-Disposition'))
        self.assertIn('attachment; filename="psycho_target_mapping.xlsx"', response['Content-Disposition'])

    def test_import_excel_csv(self):
        """Verify that importing massive data from a CSV/Excel file works properly."""
        self.client.login(username=self.username, password=self.password)
        
        # Create an in-memory CSV file using pandas
        csv_data = pd.DataFrame([
            {
                'nombre': 'Julian Assange',
                'empresa': 'WikiLeaks',
                'telefono': '+44 700 000 000',
                'direccion': 'Belmarsh, UK',
                'latitud': 51.5074,
                'longitud': -0.1278,
                'ocean_o': 90,
                'ocean_c': 80,
                'ocean_e': 50,
                'ocean_a': 50,
                'ocean_n': 70,
                'intereses': 'Libertad de prensa, Transparencia, Cifrado'
            }
        ])
        
        csv_buffer = io.BytesIO()
        csv_data.to_csv(csv_buffer, index=False)
        csv_buffer.seek(0)
        
        # Mock file upload
        csv_file = io.BytesIO(csv_buffer.read())
        csv_file.name = "import_test.csv"
        
        response = self.client.post(reverse('importar_excel'), {
            'excel_file': csv_file
        })
        
        # Should redirect back to dashboard
        self.assertRedirects(response, reverse('dashboard'))
        
        # Verify Julian Assange is imported and has calculated triggers
        assange = Cliente.objects.filter(nombre='Julian Assange').first()
        self.assertIsNotNone(assange)
        self.assertEqual(assange.empresa, "WikiLeaks")
        self.assertEqual(assange.ocean_o, 90)
