from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("", views.home_view, name="home"),
    path("registro/", views.registro_view, name="registro"),
    path("login/", views.login_view, name="login"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
    path("perfil/", views.perfil_view, name="perfil"),
    
    path('revision/', views.revision, name='revision'),
    path('planificacion/', views.planificacion, name='planificacion'),
    path('desarrollo/', views.desarrollo, name='desarrollo'),
    path('enviar/', views.enviar, name='enviar'),
    path('reunion/', views.reunion, name='reunion'),
    
    # Rutas agregadas para integración
    path('diagnostico/', views.diagnostico_view, name='diagnostico'),
    path('tutor-ia/', views.tutor_ia_view, name='tutor_ia'),
    path('panel-progreso/', views.panel_progreso_view, name='panel_progreso'),
]