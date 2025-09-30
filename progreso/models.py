from django.db import models
from django.conf import settings  # Para AUTH_USER_MODEL
from aprendizaje.models import Modulo
from django.utils import timezone

class ProgresoModulo(models.Model):
    ESTADOS = [
        ('disponible', 'Disponible'),
        ('en_curso', 'En curso'),
        ('completado', 'Completado'),
    ]
    
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='disponible')
    progreso = models.IntegerField(default=0, help_text="Porcentaje de avance")
    fecha_inicio = models.DateTimeField(null=True, blank=True)
    fecha_fin = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.usuario} - {self.modulo.titulo if self.modulo else 'Sin módulo'} ({self.estado})"

    def marcar_en_curso(self):
        if self.estado == 'disponible':
            self.estado = 'en_curso'
            self.fecha_inicio = timezone.now()
            self.save()

    def marcar_completado(self):
        if self.estado == 'en_curso':
            self.estado = 'completado'
            self.progreso = 100
            self.fecha_fin = timezone.now()
            self.save()