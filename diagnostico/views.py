from django.shortcuts import render

def index(request):
    return render(request, "diagnostico/index.html")

def detalle(request, pk):
    return render(request, "diagnostico/detalle.html", {"pk": pk})