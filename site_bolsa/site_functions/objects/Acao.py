from utils import data_utils
from utils import downloader
import numpy as np

class Acao(object):
    """A simple representation of a stock.

    :param codigo: A string, the stock's code from Quandl API.
    :param precos_historicos: A list of floats, the stock's historical prices
        from the past two years.
    :param retorno_diario: A list of floats, ...
    :param retorno_esperado: A float, ...
    :param relacao: A float, ...
    """

    def __init__(self, codigo):
        self.codigo = codigo
        self.precos_historicos = self.get_precos()
        self.retorno_diario = self.calcular_retorno_diario()
        self.retorno_esperado = self.get_retorno_esperado()
        self.relacao = 0

    def get_precos(self, data_inicial=0, data_final=0):
        arq = data_utils.get_arquivo('PREÇOS', self.codigo, '.csv')
        precos = data_utils.ler_arquivo_csv(arq)
        return precos

    def calcular_retorno_diario(self):
        retorno_diario = [0]
        if len(self.precos_historicos)<=1:
            return retorno_diario
        retorno_diario = np.zeros(len(self.precos_historicos)-1)
        for i in range(len(self.precos_historicos)-1):
            retorno_diario[i] = (self.precos_historicos[i+1] - self.precos_historicos[i])/self.precos_historicos[i]
        return retorno_diario

    def get_retorno_esperado(self):
        retorno_esperado_diario = np.mean(self.retorno_diario)
        return ((1 + retorno_esperado_diario)**30) - 1

    def calcular_risco(self):
        return np.std(self.retorno_diario)

    def calcular_beta(self, retorno_diario_mercado):
        tamanho_acao = len(self.retorno_diario)
        tamanho_menor = len(retorno_diario_mercado)
        if tamanho_acao < tamanho_menor:
            tamanho_menor = tamanho_acao
        covariancia = np.cov(self.retorno_diario[:tamanho_menor], retorno_diario_mercado[:tamanho_menor], ddof=0)[0,1]
        return covariancia/np.var(retorno_diario_mercado)

    def calcular_retorno_requerido(self, retorno_livre_risco, mercado):
        beta = self.calcular_beta(mercado.retorno_diario)
        return retorno_livre_risco + beta*(mercado.retorno_esperado - retorno_livre_risco)
