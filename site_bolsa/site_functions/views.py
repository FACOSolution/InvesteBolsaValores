from django.shortcuts import render
from .objects.Carteira import Carteira

def index(request):
    teste = 'Fala vagabundo'
    return render(request, 'site_functions/index.html', {'teste': teste,})

def mostrar_grafico(request):
    if request.method == 'POST':
        tamanho = int(request.POST.get('tamanho', False))
        print(type(tamanho))
        juros = request.POST.get('juros', False)
        mercado = request.POST.get('mercado', False)
        metodo = request.POST.get('metodo', False)
        c = Carteira(tamanho, mercado, metodo)

        print('passou aqui')
        return render(request, 'site_functions/grafico.html', {'carteira': c})
    else:
        return render(request, 'site_functions/index.html')
