from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from datetime import datetime  # Añadido para la fecha en el certificado
from progreso.models import ProgresoModulo
from .models import Diagnostico, Cuestionario, Pregunta
from django.conf import settings
import json

@login_required
def diagnostico_view(request):
    cuestionario = Cuestionario.objects.first()
    if not cuestionario:
        return render(request, 'aprendizaje/diagnostico.html', {'error': 'No hay cuestionarios disponibles'})

    if request.method == 'POST':
        respuestas = {}
        for pregunta in cuestionario.preguntas.all():
            respuestas[str(pregunta.id)] = request.POST.get(f'pregunta_{pregunta.id}')
        diagnostico = Diagnostico.objects.create(
            usuario=request.user,
            cuestionario=cuestionario,
            respuestas=json.dumps(respuestas)
        )
        return redirect('panel_progreso')

    return render(request, 'aprendizaje/diagnostico.html', {'cuestionario': cuestionario})

@login_required
def modulos_disponibles(request):
    progresos = ProgresoModulo.objects.filter(usuario=request.user, estado='disponible')
    return render(request, 'aprendizaje/modulos_disponibles.html', {'progresos': progresos})

@login_required
def modulos_en_curso(request):
    progresos = ProgresoModulo.objects.filter(usuario=request.user, estado='en_curso')
    return render(request, 'aprendizaje/modulos_en_curso.html', {'progresos': progresos})

@login_required
def modulos_completados(request):
    progresos = ProgresoModulo.objects.filter(usuario=request.user, estado='completado')
    return render(request, 'aprendizaje/modulos_completados.html', {'progresos': progresos})

@login_required
def panel_progreso(request):
    disponibles = ProgresoModulo.objects.filter(usuario=request.user, estado='disponible').count()
    en_curso = ProgresoModulo.objects.filter(usuario=request.user, estado='en_curso').count()
    completados = ProgresoModulo.objects.filter(usuario=request.user, estado='completado').count()
    total = disponibles + en_curso + completados
    avance = (completados / total * 100) if total > 0 else 0
    context = {
        'disponibles': disponibles,
        'en_curso': en_curso,
        'completados': completados,
        'avance': avance,
    }
    if disponibles + en_curso == 0:
        context['certificado_disponible'] = True
    return render(request, 'aprendizaje/panel_progreso.html', context)

@login_required
def generar_certificado(request):
    if ProgresoModulo.objects.filter(usuario=request.user, estado__in=['disponible', 'en_curso']).exists():
        return HttpResponse("No has completado todos los módulos.", status=400)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="certificado.pdf"'
    p = canvas.Canvas(response, pagesize=letter)
    p.drawString(100, 750, f"Certificado de Finalización para {request.user.get_full_name()}")
    p.drawString(100, 730, "Ha completado la capacitación en competencias digitales.")
    p.drawString(100, 710, f"Fecha: {datetime.now().strftime('%Y-%m-%d')}")
    p.drawString(100, 690, "Firma: DijiTutor")
    p.save()
    return response

@login_required
def tutor_ia_view(request):
    faq = [
        {"pregunta": "¿Qué es seguridad digital?", "respuesta": "Es el uso seguro de internet para evitar phishing, virus, etc."},
        {"pregunta": "¿Cómo manejar herramientas ofimáticas?", "respuesta": "Usa Word para documentos, Excel para datos, etc."},
    ]
    if request.method == 'POST':
        pregunta_usuario = request.POST.get('pregunta')
        respuesta = next((item['respuesta'] for item in faq if pregunta_usuario.lower() in item['pregunta'].lower()), "No tengo respuesta para eso. Prueba otra pregunta.")
        return render(request, 'aprendizaje/tutor_ia.html', {'faq': faq, 'respuesta': respuesta})
    return render(request, 'aprendizaje/tutor_ia.html', {'faq': faq})