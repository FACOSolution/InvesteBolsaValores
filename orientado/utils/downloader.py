from datetime import date
import quandl

quandl.ApiConfig.api_key = 'xX62DrpcmpMS3k3moVeh'

hoje = date.today()
data_inicial = date(hoje.year - 2, hoje.month, hoje.day)
data_inicial = '{:%Y-%m-%d}'.format(data_inicial)
data_final = hoje
data_final = '{:%Y-%m-%d}'.format(data_final)

caminho = '{:%d-%m-%Y}'.format(hoje)

def baixar_precos_acao(codigo_acao):
    dataset = 'GOOG/BVMF_' + codigo_acao
    precos = []
    try:
        precos = quandl.get(dataset, start_date=data_inicial,
        end_date=data_final, column_index=4)
    except quandl.errors.quandl_error.QuandlError:
        return [False, precos]

    return [True, precos]

def baixar_pontuacoes_mercado(codigo):
    dataset = 'YAHOO/' + codigo
    pontuacoes = []
    pontuacoes = quandl.get(dataset, start_date=data_inicial,
     end_date=data_final, column_index=4)
    return pontuacoes

def baixar_taxa_selic():
    taxa = []
    taxa = quandl.get('BCB/11', start_date=data_inicial,
     end_date=data_final, limit=1, column_index=1)
    return taxa
