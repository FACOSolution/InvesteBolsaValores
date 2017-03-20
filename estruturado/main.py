# Contém as funções que manipulam arquivos.
import arquivos as arq
# Contém as funções que fazem os cálculos necessários para a apliacação.
import calc
# Contém a função que extrai a composição da carteira IBOVESPA do site oficial.
import scrapper
# Contém as funções que adquirem os dados da API Quandl.
import dados
# Determina o caminho da sistema.
import os.path
# Função para criar pasta.
from os import mkdir

# Criar pasta, caso não exista, para guardar os arquivos com os dados.
# A aquisição dos dados SÓ ESTÁ SENDO EXECUTADA UMA ÚNICA VEZ POR DIA, já que
# depende que a pasta não exista.
if not os.path.exists(dados.caminho):
    print('\nCriando pasta ' + dados.caminho + ' ...')
    mkdir(dados.caminho)
    print('\nBaixando composição da carteira IBOVESPA...')
    scrapper.baixar_composicao_carteira_ibovespa()
    print('\nAcessando API Quandl para extração de preços...')
    dados.baixar_dados_quandl()

# Ler arquivo csv do mercado
"""
# Assumindo que o arquivo de mercado foi baixado com este nome INDEX_BVSP.
# Existe a possibilidade de algum problema com o arquivo. Então, assumi que será
# retornada uma lista com dois valores. Na posição [0], não houve problemas se vier
# True, e na posição [1], não houve problemas se vierem a lista com os preços.
    # return [False, None] ou return [True, precos]"""
precos_mercado = arq.ler_arquivo_csv('INDEX_BVSP')[1]

# Ler arquivo csv da taxa selic
"""
# Assumindo que a taxa selic foi também baixada para um arquivo csv com o nome SELIC.
# Será retornada uma lista com apenas uma taxa selic, a mais recente."""
taxas_selic = arq.ler_arquivo_csv('SELIC')[1]
retorno_livre_risco = taxas_selic[0]/100

# Ler arquivo txt com nomes de ações
"""
# Assumindo que os nomes(códigos) das ações estão num arquivo AÇÕES_IBOVESPA.
# Com esses códigos serão abertos os arquivos csv de cada ação, também assumindo
# que o nome dos arquivos é [código].csv
    # ABEV3.csv"""
acoes = arq.ler_arquivo_txt('AÇÕES_IBOVESPA')

"""
# A ideia é termos todas as ações da IBOVESPA numa lista. Para cada ação são feitos
# cálculos onde a ação ou é descartada ou é uma candidata à entrar na carteira.

# As ações candidatas a formar a carteira ou portfólio seriam aquelas em que
# retorno_requerido é menor do que o retorno_esperado. A ação sendo uma candidata
# será calculada a relação (retorno esperado/beta).

# Ao final, teremos uma lista de candidatas das quais "X" ações com maiores
# relações (retorno_esperado/beta) serão selecionadas para formar a carteira ou
# portifólio.

# Em seguida serão calculados os valores desta carteira: retorno esperado, risco, beta e etc.
"""

# Lista com ações candidatas à entrarem na carteira.
candidatas = []

qtd_avaliada = 0
for acao in acoes:
    # Retirar o '\n' de cada código.print('Entrou')
    codigo = acao[0:-1]
    # Ler arquivo csv da ação.
    resposta = arq.ler_arquivo_csv(codigo)
    # Se a leitura ocorrer sem problemas, os cálculos da ação são efetudados.
    if resposta[0] == True:
        qtd_avaliada = qtd_avaliada + 1
        precos = resposta[1]
        # Para calcular a covariância a lista com os preços do mercado devem ser
        # do mesmo tamanho da lista com os preços da ação. Escolhe-se o menor.
        tamanho_mercado = len(precos_mercado)
        tamanho_acao = len(precos)
        tamanho_menor = tamanho_mercado
        if tamanho_acao < tamanho_mercado:
            tamanho_menor = tamanho_acao

        # Do mercado necessitamos o retorno diário
        retorno_diario_mercado = calc.get_retorno_diario(precos_mercado, tamanho_menor)

        # Da ação necessitamos os retornos diário, esperado e requerido.
        retorno_diario = calc.get_retorno_diario(precos, tamanho_menor)
        retorno_esperado = calc.get_retorno_esperado(retorno_diario)
        retorno_requerido = calc.get_retorno_requerido(retorno_diario, retorno_diario_mercado, retorno_livre_risco)

        # Se o retorno requerido for maior do que o retorno esperado, a ação é
        # descartada. Caso contrário será uma das candidatas a entrarem na
        # carteira.

        if retorno_requerido < retorno_esperado:
            beta = calc.calcular_beta(retorno_diario, retorno_diario_mercado)
            relacao = retorno_esperado/beta
            # Como uma candidata, necessitamos das informações sobre o código,
            # relação, retorno_esperado e beta para futuros cálculos.
            # Apesar da relação ser um valor que pode ser calculado com as outras
            # informações, necessitamos dela para ordenamos a lista de candidatas
            # pelas maiores relações.
            candidata = [codigo, relacao, retorno_esperado, beta]
            candidatas.append(candidata)

# As ações candidatas serão ordenadas por maior relação e {tamanho_carteira} serão
# selecionadas para formar a carteira.
tamanho_carteira = 10
print('\n\tAÇÕES IBOVESPA..........: ', len(acoes))
print('\tAÇÕES AVALIADAS.........: ', qtd_avaliada)
print('\tAÇÕES NÃO DESCARTADAS...: ', len(candidatas))
print('\tAÇÕES DA CARTEIRA.......: ', tamanho_carteira)
print('\n\t\tCOMPOSIÇÃO\n\tAÇÃO\tRELAÇÃO (RE/BETA)\n')
carteira = calc.montar_carteira(candidatas, tamanho_carteira)
x_data = []
y_data = []
for acao in carteira:
    print('\t%s\t%f' % (acao[0], acao[1]))

# Em seguida, é calculado o retorno_esperado e o beta da carteira.
print('\nRetorno Esperado da Carteira em % : ', calc.get_retorno_esperado_carteira(carteira)*100)
print('Beta da Carteira : ',calc.get_beta_carteira(carteira))
