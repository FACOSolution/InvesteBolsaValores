from django.shortcuts import render


def index(request):
    return render(request, 'site_functions/index.html')

def mostrar_grafico(request):
    print('passou aqui')
    return render(request, 'site_functions/grafico.html')
