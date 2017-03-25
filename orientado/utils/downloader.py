from datetime import date
import pandas
import quandl

quandl.ApiConfig.api_key = 'xX62DrpcmpMS3k3moVeh'

hoje = date.today()
data_inicial = date(hoje.year - 2, hoje.month, hoje.day)
data_inicial = '{:%Y-%m-%d}'.format(data_inicial)
data_final = hoje
data_final = '{:%Y-%m-%d}'.format(data_final)

caminho = '{:%d-%m-%Y}'.format(hoje)

def acessar_quandl(dataset='', start_date=data_inicial, end_date=data_final, column_index=0):

    try:
        dados = quandl.get(dataset, start_date=data_inicial,
        end_date=data_final, column_index=column_index)
    except quandl.errors.quandl_error.QuandlError:
        dados = pandas.DataFrame()

    return dados

def baixar_precos_acao(codigo_acao):
    dataset = 'GOOG/BVMF_' + codigo_acao
    precos = acessar_quandl(dataset, column_index = 4)
    return precos

def baixar_pontuacoes_mercado(codigo):
    dataset = 'YAHOO/' + codigo
    pontuacoes = acessar_quandl(dataset, column_index = 4)
    return pontuacoes

def baixar_taxa_selic():
    dataset = 'BCB/4390'
    taxa = acessar_quandl(dataset, column_index = 1)
    return taxa
