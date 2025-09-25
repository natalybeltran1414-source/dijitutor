from django.urls import path
from . import views
urlpatterns = [
    path("", views.index, name="index"),
    path("detalle/<int:pk>/", views.detalle, name="detalle"),
]