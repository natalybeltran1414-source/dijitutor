from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
import json

class Area(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

class Modulo(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    duracion_estimada = models.IntegerField(help_text="En minutos", default=60)
    contenido = models.TextField(blank=True)  # Contenido o enlaces

    def __str__(self):
        return self.titulo

class Pregunta(models.Model):
    texto = models.TextField()
    opciones = models.JSONField(default=list)  # e.g., [{"texto": "Opción A", "correcta": True}, ...]
    area = models.ForeignKey(Area, on_delete=models.CASCADE)  # Asociada a un área para diagnóstico

    def __str__(self):
        return self.texto[:50]

class Cuestionario(models.Model):
    titulo = models.CharField(max_length=200)
    preguntas = models.ManyToManyField(Pregunta)  # 3-5 preguntas por área/módulo

    def __str__(self):
        return self.titulo

class Diagnostico(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cuestionario = models.ForeignKey(Cuestionario, on_delete=models.CASCADE)
    respuestas = models.JSONField(default=dict)  # Respuestas del usuario
    puntuacion = models.IntegerField(default=0)  # Puntuación total
    brechas = models.JSONField(default=list)  # Áreas débiles como JSON list, e.g., ["seguridad digital"]
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Diagnóstico de {self.usuario} - {self.puntuacion}"

    def calcular_brechas(self):
        # Lógica simple: Si puntuación por área < 70%, agregar brecha
        # Asume que respuestas tienen keys como 'pregunta_id': respuesta
        # Calcula puntuación y brechas aquí (puedes expandir)
        total_correctas = 0
        brechas_list = []
        for pregunta in self.cuestionario.preguntas.all():
            respuesta_usuario = self.respuestas.get(str(pregunta.id))
            opcion_correcta = next((op for op in pregunta.opciones if op.get('correcta')), None)
            if respuesta_usuario == opcion_correcta.get('texto') if opcion_correcta else False:
                total_correctas += 1
        self.puntuacion = (total_correctas / self.cuestionario.preguntas.count()) * 100 if self.cuestionario.preguntas.count() > 0 else 0
        if self.puntuacion < 70:
            brechas_list.append(self.cuestionario.preguntas.first().area.nombre if self.cuestionario.preguntas.exists() else "General")
        self.brechas = json.dumps(brechas_list)
        self.save()

# Signal para recomendación y asignación
@receiver(post_save, sender=Diagnostico)
def recomendar_y_asignar_modulos(sender, instance, created, **kwargs):
    if created:
        instance.calcular_brechas()  # Calcula brechas primero
        from progreso.models import ProgresoModulo
        try:
            brechas_list = json.loads(instance.brechas)
            modulos_recomendados = Modulo.objects.filter(area__nombre__in=brechas_list)
            for modulo in modulos_recomendados:
                ProgresoModulo.objects.get_or_create(
                    usuario=instance.usuario,
                    modulo=modulo,
                    defaults={'estado': 'disponible'}
                )
        except json.JSONDecodeError:
            pass
