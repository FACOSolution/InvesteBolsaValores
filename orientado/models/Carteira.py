from utils import scrapper
from utils import data_utils
from .Acao import Acao
from .Mercado import Mercado

class Carteira(object):

    def __init__(self, retorno_livre_risco=0.5, tamanho=10, mercado='IBOVESPA', metodo='RELAÇÃO'):
        self.mercado = Mercado(mercado)
        self.retorno_livre_risco = retorno_livre_risco
        self.tamanho = tamanho
        self.aplicar_metodo(metodo)
        self.acoes = []

    
    def aplicar_metodo(self, metodo):
        pass

    def ordenar_acoes(self):
        pass

    def calcular_retorno_esperado(self):
        tamanho = len(carteira)
        retorno_esperado = 0
        for acao in carteira:
            retorno_esperado += acao[2]*(1/tamanho)
        return retorno_esperado

    def calcular_beta(self):
        tamanho = len(carteira)
        beta = 0
        for acao in carteira:
            beta += acao[3]*(1/tamanho)
        return beta
