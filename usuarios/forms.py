from django.contrib.auth.forms import UserCreationForm
from .models import Usuario
from django import forms

class RegistroForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

        labels = {
            "username": "Nombre de usuario",
            "email": "Correo electrónico",
            "first_name": "Nombre",
            "last_name": "Apellido",
            "rol": "Rol",
            "password1": "Contraseña",
            "password2": "Confirmar contraseña",
        }