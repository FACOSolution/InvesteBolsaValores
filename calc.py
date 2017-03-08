"""NumPy é um pacote para computação científica.
Contém as funções estatísticas utilizadas"""
import numpy as np
"""itemgetter auxilia a ordenação de uma lista de listas de mesma forma.
A ordenação é feita baseada num índice em comum."""
from operator import itemgetter

"""O retorno diário é dado pela seguinte fórmula:
   (preço de fechamento - preço de abertura)/preço de abertura.
Como é um histórico de preços, teremos um retorno para cada dia."""
def get_retorno_diario(preco, tamanho):
    # A lista de retornos diários é uma unidade menor do que a lista de preços.
    # Inicializa-se essa lista com zeros.
    retorno_diario = np.zeros(tamanho-1)
    # Aplica-se a fórmula já citada.
    for i in range(tamanho-1):
        retorno_diario[i] = (preco[i+1] - preco[i])/preco[i]
    return retorno_diario

"""O retorno esperado ou retorno médio é a média aritmética dos retornos diários"""
def get_retorno_esperado(retorno_diario):
    # A função mean(NumPy) calcula a média aritmética.
    return np.mean(retorno_diario)

"""O risco é o desvio-padrão dos retornos diários"""
def get_risco(retorno_diario):
    # A função std(NumPy) calcula o desvio-padrão.
    return np.std(retorno_diario)

"""O beta é dado pela seguinte fórmula:
    Covariância(Ri,Rm)/Variância(Rm)
    Ri = retornos do título; Rm = retornos da carteira de mercado"""
def calcular_beta(retorno_diario_acao, retorno_diario_mercado):
    # A função cov(Numpy) retorna a matriz de covariância das variáveis.
    # A covariância que nos interessa está na posição [0,1] desta matriz.
    covariancia = np.cov(retorno_diario_acao, retorno_diario_mercado, ddof=0)[0,1]
    return covariancia/np.var(retorno_diario_mercado)

"""O retorno requerido é dado pela seguinte fórmula:
    Rf + beta[i](REm - Rf)
    Rf = retorno livre de risco (taxa Selic será usada)
    REm = retorno esperado da carteira de mercado
    beta[i] = beta do ativo(ação) i"""
def get_retorno_requerido(retorno_diario_acao, retorno_diario_mercado, retorno_livre_risco):
    beta = calcular_beta(retorno_diario_acao, retorno_diario_mercado)
    retorno_esperado_mercado = get_retorno_esperado(retorno_diario_mercado)
    
    return retorno_livre_risco + beta*(retorno_esperado_mercado - retorno_livre_risco)

"""Selecionar [tamanho] maiores ações com maiores (retorno_esperado/beta)"""
def montar_carteira(candidatas, tamanho):
    # Ordenar pela maior relação RE/beta. A relação é a posição (1) de cada ação.
    candidatas.sort(key=itemgetter(1), reverse=True)
    carteira = []
    # Inserir na carteira as [tamanho] maiores
    for i in range(tamanho):
        carteira.append(candidatas[i])
    return carteira

"""O retorno esperado da carteira de ativos é dado pela seguinte fórmula:
    Somatório(Xi*REi)
    Xi = é a participação do ativo na carteira. (Inicialmente será usado uma
    participação igual para todas. 1/tamanho)
    REi = retorno esperado do ativo i"""
def get_retorno_esperado_carteira(carteira):
    tamanho = len(carteira)
    retorno_esperado = 0
    for acao in carteira:
        # O retorno esperado é a posição [2] de cada ação.
        retorno_esperado += acao[2]*(1/tamanho)
    return retorno_esperado

"""O beta da carteira de ativos é dado pela seguinte fórmula:
    Somatório(Xi*beta[i])
    Xi = é a participação do ativo na carteira. (Inicialmente será usado uma
    participação igual para todas. 1/tamanho)
    beta[i] = beta do ativo i"""
def get_beta_carteira(carteira):
    tamanho = len(carteira)
    beta = 0
    for acao in carteira:
        # O beta é posição (3) de cada ação.
        beta += acao[3]*(1/tamanho)
    return beta
