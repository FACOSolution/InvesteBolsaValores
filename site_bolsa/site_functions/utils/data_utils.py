from . import downloader
from . import scrapper
from datetime import date
from os.path import join
from os import mkdir
import os.path
import csv

hoje = date.today()
hoje = '{:%d-%m-%Y}'.format(hoje)

# caminho = hoje + '/' + nome + '.csv'
caminho = join(os.getcwd(), 'datasets')

def ler_arquivo_csv(nome, pos=0):
    precos = []
    with open(nome, 'r') as arq:
        reader = csv.reader(arq)
        for linha in reader:
            precos.append(float(linha[pos]))
    return precos

def escrever_csv(nome, dados, index=False, header=False):
    dados.to_csv(join(caminho, nome + '.csv'), index=index, header=header)

def ler_arquivo_txt(nome):
    acoes = []
    with open(nome, 'r') as arq:
        for linha in arq:
            acoes.append(linha[0:-1])
    return acoes

def escrever_lista_em_txt(nome, lista):
    codigos = []
    with open(join(caminho, nome + '.txt'), 'w') as arq:
        for codigo in lista:
            codigo = codigo + '\n'
            codigos.append(codigo)
        arq.writelines(codigos)

def baixar_e_gravar(tipo, codigo_quandl):
    if tipo == 'COMPOSIÇÃO':
        print('Baixando composição carteira IBOVESPA...')
        composicao = scrapper.get_composicao_carteira_ibovespa()
        escrever_lista_em_txt('COMPOSIÇÃO IBOVESPA', composicao)
    elif tipo == 'PONTUAÇÕES':
        print('Baixando pontuações ' + codigo_quandl + '...')
        pontuacoes = downloader.baixar_pontuacoes_mercado(codigo_quandl)
        escrever_csv(codigo_quandl, pontuacoes)
    elif tipo == 'PREÇOS':
        print('Baixando preços históricos ' + codigo_quandl + '...')
        precos = downloader.baixar_precos_acao(codigo_quandl)
        escrever_csv(codigo_quandl, precos)
    else:
        print('Baixando Taxa SELIC...')
        taxa = downloader.baixar_taxa_selic()
        escrever_csv('SELIC', taxa)

def get_arquivo(tipo, codigo_quandl, formato):
    caminho_arquivo = join(caminho, codigo_quandl + formato)

    if not os.path.exists(caminho):
        print('\nCriando pasta ' + caminho + ' ...')
        mkdir(caminho)
    try:
        open(caminho_arquivo, 'r')
    except:
        baixar_e_gravar(tipo, codigo_quandl)

    return caminho_arquivo
