from django.db import models

class Cliente(models.Model):
    nombre = models.CharField(max_length=255, verbose_name="Nombre Completo")
    empresa = models.CharField(max_length=255, blank=True, null=True, verbose_name="Empresa / Rubro")
    telefono = models.CharField(max_length=50, blank=True, null=True, verbose_name="Teléfono")
    direccion = models.CharField(max_length=255, blank=True, null=True, verbose_name="Dirección")
    latitud = models.FloatField(verbose_name="Latitud")
    longitud = models.FloatField(verbose_name="Longitud")
    
    # OCEAN Scores (0-100)
    ocean_o = models.IntegerField(default=50, verbose_name="Apertura (Openness)")
    ocean_c = models.IntegerField(default=50, verbose_name="Responsabilidad (Conscientiousness)")
    ocean_e = models.IntegerField(default=50, verbose_name="Extraversión (Extraversion)")
    ocean_a = models.IntegerField(default=50, verbose_name="Amabilidad (Agreeableness)")
    ocean_n = models.IntegerField(default=50, verbose_name="Neuroticismo (Neuroticism)")
    
    # Behavior & Marketing Predictions
    comportamiento_compra = models.CharField(max_length=100, blank=True, verbose_name="Comportamiento de Compra")
    estilo_decision = models.CharField(max_length=100, blank=True, verbose_name="Estilo de Decisión")
    disparadores_compra = models.TextField(blank=True, null=True, verbose_name="Disparadores de Venta")
    intereses = models.TextField(blank=True, null=True, verbose_name="Intereses Clave")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Auto-compute psychographic predictions if not explicitly set
        if not self.comportamiento_compra:
            self.comportamiento_compra = self.compute_comportamiento()
        if not self.estilo_decision:
            self.estilo_decision = self.compute_estilo_decision()
        if not self.disparadores_compra:
            self.disparadores_compra = self.compute_disparadores()
        super().save(*args, **kwargs)

    def compute_comportamiento(self):
        scores = {
            'O': self.ocean_o,
            'C': self.ocean_c,
            'E': self.ocean_e,
            'A': self.ocean_a,
            'N': self.ocean_n
        }
        # Find dominant trait, but use custom conditions
        if scores['O'] >= 70 and scores['E'] >= 60:
            return "Impulsivo e Innovador"
        elif scores['C'] >= 70:
            return "Racional y Analítico"
        elif scores['N'] >= 70:
            return "Reactivo y Sensible al Riesgo"
        elif scores['A'] >= 70:
            return "Social y Leal"
        
        # Fallback to absolute maximum
        max_trait = max(scores, key=scores.get)
        if max_trait == 'O': return "Explorador / Adaptable"
        if max_trait == 'C': return "Metódico y Preciso"
        if max_trait == 'E': return "Entusiasta / Social"
        if max_trait == 'A': return "Colaborativo"
        return "Prudente / Conservador"

    def compute_estilo_decision(self):
        if self.ocean_c >= 65:
            return "Basado en Datos / Lógico"
        elif self.ocean_e >= 65 and self.ocean_o >= 60:
            return "Emocional / Espontáneo"
        elif self.ocean_a >= 65:
            return "Consensuado / Social"
        elif self.ocean_n >= 65:
            return "Evitación de Riesgos"
        return "Pragmático / Funcional"

    def compute_disparadores(self):
        triggers = []
        if self.ocean_o >= 65:
            triggers.append("Innovación y Exclusividad")
        if self.ocean_c >= 65:
            triggers.append("Métricas de Calidad / Retorno de Inversión")
        if self.ocean_e >= 65:
            triggers.append("Estatus y Reconocimiento")
        if self.ocean_a >= 65:
            triggers.append("Atención Personalizada y Testimonios")
        if self.ocean_n >= 65:
            triggers.append("Garantía de Devolución / Soporte Permanente")
        
        if not triggers:
            triggers.append("Soluciones Prácticas y Eficiencia")
            
        return ", ".join(triggers)

    def __str__(self):
        return f"{self.nombre} ({self.empresa or 'Sin Empresa'})"

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['-created_at']
