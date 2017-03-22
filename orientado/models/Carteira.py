from utils import scrapper
from utils import data_utils
from utils import downloader
from .Acao import Acao
from .Mercado import Mercado
import operator

class Carteira(object):

    def __init__(self, tamanho=10, mercado='IBOVESPA', metodo='RELAÇÃO'):
        self.mercado = Mercado(mercado)
        self.retorno_livre_risco = self.calcular_retorno_livre_risco()
        self.tamanho = tamanho
        self.acoes = self.mercado.acoes_mercado
        self.aplicar_metodo(metodo)


    def aplicar_metodo(self, metodo):
        if metodo == 'RELAÇÃO':
            tipo = 1
            self.acoes = self.calcular_relacao()
        self.montar_carteira(tipo)

    def montar_carteira(self, tipo):
        if tipo == 1:
            self.acoes.sort(key=operator.attrgetter('relacao'), reverse=True)
        self.acoes = self.acoes[:self.tamanho]

    def calcular_relacao(self):
        acoes_nao_descartadas = []
        tamanho_mercado = len(self.mercado.pontuacoes)
        for acao in self.acoes:

            retorno_requerido = acao.calcular_retorno_requerido(self.retorno_livre_risco, self.mercado)

            if retorno_requerido < acao.retorno_esperado and len(acao.retorno_diario) > 1:
                beta = acao.calcular_beta(self.mercado.retorno_diario)
                acao.relacao = acao.retorno_esperado/beta
                acoes_nao_descartadas.append(acao)
        return acoes_nao_descartadas

    def calcular_retorno_esperado(self):
        retorno_esperado = 0
        for acao in self.acoes:
            retorno_esperado += acao.retorno_esperado*(1/self.tamanho)
        return retorno_esperado

    def calcular_beta_carteira(self):
        beta = 0
        for acao in self.acoes:
            beta += acao.calcular_beta(self.mercado.retorno_diario)*(1/self.tamanho)
        return beta

    def calcular_retorno_livre_risco(self):
        #taxas_selic = data_utils.ler_arquivo_csv('SELIC')[1]
        #if not taxas_selic:
        taxas_selic = downloader.baixar_taxa_selic()
        data_utils.escrever_csv('SELIC', taxas_selic)
        taxas_selic = data_utils.ler_arquivo_csv('SELIC')
        retorno_livre_risco = taxas_selic[0]/100
        return retorno_livre_risco
