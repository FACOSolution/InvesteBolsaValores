from site_functions.utils import data_utils
from site_functions.utils import downloader
from site_functions.utils import scrapper
from .Acao import Acao
import numpy as np


class Mercado(object):
    """A simple representation of a market portfolio.

    :param nome: A string, ...
    :param codigo: A string, ...
    :param codigo_acoes: A list of strings, ...
    :param pontuacoes: A list of floats, ...
    :param retorno_diario: A list of floats, ...
    :param retorno_esperado: A float, ...
    :param acoes_mercado: A list of Acao objects, xxx.
    """


    def __init__(self, nome):
        self.nome = nome
        self.codigo = 'INDEX_BVSP'
        self.codigo_acoes = self.get_composicao()
        self.pontuacoes = self.get_pontuacoes()
        self.retorno_diario = self.calcular_retorno_diario()
        self.retorno_esperado = self.get_retorno_esperado()
        self.acoes_mercado = self.montar_mercado()

    def get_pontuacoes(self):
        arq = data_utils.get_arquivo('PONTUAÇÕES', self.codigo, '.csv')
        pontuacoes = data_utils.ler_arquivo_csv(arq)
        return pontuacoes

    def get_composicao(self):
        arq = data_utils.get_arquivo('COMPOSIÇÃO', 'COMPOSIÇÃO IBOVESPA', '.txt')
        composicao = data_utils.ler_arquivo_txt(arq)
        return composicao

    def calcular_retorno_diario(self):
        retorno_diario = np.zeros(len(self.pontuacoes)-1)
        for i in range(len(self.pontuacoes)-1):
            retorno_diario[i] = (self.pontuacoes[i+1] - self.pontuacoes[i])/self.pontuacoes[i]
        return retorno_diario

    def get_retorno_esperado(self):
        retorno_esperado_diario = np.mean(self.retorno_diario)
        #return retorno_esperado_diario
        return ((1 + retorno_esperado_diario)**30) - 1

    def montar_mercado(self):
        acoes = []
        for codigo in self.codigo_acoes:
            acao = Acao(codigo)
            acoes.append(acao)
        return acoes
