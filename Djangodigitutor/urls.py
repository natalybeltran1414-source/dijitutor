from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

# Vista básica para la raíz
def home(request):
    return HttpResponse("<h1>Bienvenido</h1><p>a mi me gusta alguien especial.</p>")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),  # 👈 Aquí agregamos la raíz
    path('', include('usuarios.urls')),  # 👈 Importamos las rutas de tu app usuarios
]