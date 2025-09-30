from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from aprendizaje import views

def home(request):
    return render(request, "home.html")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('', include('usuarios.urls')),
    path('modulos/disponibles/', views.modulos_disponibles, name='modulos_disponibles'),
    path('modulos/en-curso/', views.modulos_en_curso, name='modulos_en_curso'),
    path('modulos/completados/', views.modulos_completados, name='modulos_completados'),
]