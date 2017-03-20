import numpy as np
from utils import data_utils
from utils import downloader

class Acao(object):

    def __init__(self, codigo):
        self.codigo = codigo
        self.precos_historicos = self.get_precos()
        self.retorno_diario = self.calcular_retorno_diario()
        self.retorno_esperado = self.get_retorno_esperado()

    def get_precos(self, data_inicial=0, data_final=0):
        precos = data_utils.ler_arquivo_csv(self.codigo)
        print(len(precos))
        if not precos:
            print('Baixando ' + self.codigo)
            resp = downloader.baixar_precos_acao(self.codigo)
            precos = resp[1]
            if resp[0] == True:
                data_utils.escrever_csv(self.codigo, precos)
        return precos

    def calcular_retorno_diario(self):
        retorno_diario = np.zeros(len(self.precos_historicos)-1)
        for i in range(len(self.precos_historicos)-1):
            retorno_diario[i] = (self.precos_historicos[i+1] - self.precos_historicos[i])/self.precos_historicos[i]
        return retorno_diario

    def get_retorno_esperado(self):
        retorno_esperado_diario = np.mean(self.retorno_diario)
        return (1 + retorno_esperado_diario)**30

    def calcular_risco(self):
        return np.std(self.retorno_diario)

    def calcular_beta(self, retorno_diario_mercado):
        covariancia = np.cov(self.retorno_diario, retorno_diario_mercado, ddof=0)[0,1]
        return covariancia/np.var(retorno_diario_mercado)

    def calcular_retorno_requerido(self, retorno_diario_mercado, retorno_livre_risco):
        beta = calcular_beta(self.retorno_diario, retorno_diario_mercado)
        retorno_esperado_mercado = get_retorno_esperado(retorno_diario_mercado)
        return retorno_livre_risco + beta*(retorno_esperado_mercado - retorno_livre_risco)
