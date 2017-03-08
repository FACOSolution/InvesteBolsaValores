"""
OBJETIVO:   Gerar arquivos csv com os dados das ações, índice bovespa, taxa selic.
PASSOS:     1 - Estabelecer parâmetros de acesso à API QUANDL e local de gravação
                dos arquivos csv.
            2 - Obter dados ao acessar a api com os parâmetros de cada dataset buscado.
            3 - Exportar os dados para os respectivoos arquivos .csv.
            4 - Gerar relatório sobre o acesso à API.
"""
# Obter datas para acessar API.
from datetime import date
# Bilbioteca da API.
import quandl
# Contém as funções que manipulam arquivos.
import arquivos as arq
# Função para tranformar dados em um tipo DataFrame e em seguida serem salvos
# em .csv.
from pandas import DataFrame

# Chave da API obtida após cadastro no site.
quandl.ApiConfig.api_key = 'xX62DrpcmpMS3k3moVeh'

# Parâmetros de datas para acessar API. Devem estar no formato aa-mm-dd.
hoje = date.today()
# Utilizar dados históricos de 2 anos atrás até data atual.
data_inicial = date(hoje.year - 2, hoje.month, hoje.day)
data_inicial = '{:%Y-%m-%d}'.format(data_inicial)
data_final = hoje
data_final = '{:%Y-%m-%d}'.format(data_final)

# Nome da pasta, no formato dd-mm-aa, que guardará os arquivos gerados.
caminho = '{:%d-%m-%Y}'.format(hoje)


"""
# Acessar Quandl com os parâmetros passados e exportar os dados para csv.
#   nome_arquivo - nome do arquivo que será salvo. Ex: 'SELIC'
#   dataset - conjunto de dados que será consultado no Quandl. Ex: 'YAHOO/INDEX_BVSP'
#   start_date, end_date - datas inicial e final, respectivamente.
#   qtd - refere-se a quantidade de linhas que com valores que desejo receber.
#       0 - recebe todas delimitadas pelas datas. Utilizadas nas ações e índice bovespa.
#       1 - recebe apenas 1 linha, a mair recente. Utilizada na TAXA SELIC. Apenas a do dia.
#   index - índice da coluna da qual desejo receber valores.
#           A coluna que contém o preço de fechamento das ações e índice bovespa é 4.
#           Na Taxa Selic, o valor encontra-se na coluna 1.
"""
def acessar_quandl(nome_arquivo, dataset, start_date=data_inicial, end_date=data_final, qtd=0, index=4):
    # Se não houver erros ao acessar a API, os dados são salvos no caminho e local
    # especificado e, retornam dados para montar o relátorio final. Caso contrário,
    # o erro ocorrido é transformado em texto que será colocado no relatório.
    try:
        dados = quandl.get(dataset, start_date=data_inicial, end_date=data_final, limit=qtd,column_index=index)
        dados.to_csv(caminho + '/' + nome_arquivo + '.csv', index=False, header=False)
        return (nome_arquivo, True, '')
    except quandl.errors.quandl_error.QuandlError as erro:
        return (nome_arquivo, False, str(erro))


def baixar_dados_quandl():

    # Lista com as informações sobre o acesso da API para fins de controle.
    relatorio = []

    # Pegar preços do mercado
    relatorio.append(acessar_quandl('INDEX_BVSP', 'YAHOO/INDEX_BVSP'))

    # Pegar valor da taxa selic
    relatorio.append(acessar_quandl('SELIC', 'BCB/11', qtd=1, index=1))

    # Pegar preços das ações
    acoes = arq.ler_arquivo_txt('AÇÕES_IBOVESPA')

    for acao in acoes:
        codigo = acao[0:-1]
        dataset = 'GOOG/BVMF_' + codigo
        relatorio.append(acessar_quandl(codigo, dataset))

    # Salvar relátorio em arquivo csv.
    dados_relatorio = DataFrame(relatorio, columns=['Código', 'Sucesso', 'Msg_erro'])
    dados_relatorio.to_csv(caminho + '/RELATÓRIO.csv',index=False)
