import numpy as np
from utils import data_utils
from utils import downloader

class Acao(object):

    def __init__(self, codigo):
        self.codigo = codigo
        self.precos_historicos = self.get_precos()
        self.retorno_diario = self.calcular_retorno_diario()
        self.retorno_esperado = self.get_retorno_esperado()
        self.relacao = None

    def get_precos(self, data_inicial=0, data_final=0):
        precos = data_utils.ler_arquivo_csv(self.codigo)
        print(len(precos))
        if not precos:
            print('Baixando ' + self.codigo)
            resp = downloader.baixar_precos_acao(self.codigo)
            precos = resp[1]
            if resp[0] == True:
                data_utils.escrever_csv(self.codigo, precos)
                precos = data_utils.ler_arquivo_csv(self.codigo)
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
        return retorno_esperado_diario
        #return (1 + retorno_esperado_diario)**30

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
