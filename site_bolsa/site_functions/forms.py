from django import forms
from .models import *
class PortfolioForm(forms.ModelForm):

    tamanho = forms.CharField(label='Tamanho da Carteira')
    #juros = forms.CharField(label='Taxa de Juros')
    mercado = forms.CharField(label='Carteira de Mercado')
    metodo = forms.CharField(label='Método a ser aplicado')
    class Meta:
		model = Carteira
		fields = ('tamanho','mercado', 'metodo',)
