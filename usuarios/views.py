from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegistroForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required


def registro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            return redirect('perfil')
    else:
        form = RegistroForm()
    return render(request, 'usuarios/registro.html', {'form': form})

@login_required
def perfil_view(request):
    return render(request, 'usuarios/perfil.html', {'user': request.user})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('perfil')
    else:
        form = AuthenticationForm()
    return render(request, 'usuarios/login.html', {'form': form})

# 👇 Por si quieres añadir más adelante
def diagnostico_view(request):
    return render(request, 'usuarios/diagnostico.html')


def home_view(request):
    return render(request, "home.html")

def revision(request):
    return render(request, 'usuarios/revision.html')

@login_required
def planificacion(request):
    return render(request, 'usuarios/planificacion.html')

@login_required
def desarrollo(request):
    return render(request, 'usuarios/desarrollo.html')

@login_required
def enviar(request):
    return render(request, 'usuarios/enviar.html')

@login_required
def reunion(request):
    return render(request, 'usuarios/reunion.html')
