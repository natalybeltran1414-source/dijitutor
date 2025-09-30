from django.urls import path
from . import views

urlpatterns = [
    path('diagnostico/', views.diagnostico_view, name='diagnostico'),
    path('modulos/disponibles/', views.modulos_disponibles, name='modulos_disponibles'),
    path('modulos/en-curso/', views.modulos_en_curso, name='modulos_en_curso'),
    path('modulos/completados/', views.modulos_completados, name='modulos_completados'),
    path('panel-progreso/', views.panel_progreso, name='panel_progreso'),
    path('generar-certificado/', views.generar_certificado, name='generar_certificado'),
    path('tutor-ia/', views.tutor_ia_view, name='tutor_ia'),
]