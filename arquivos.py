import csv
from datetime import date

hoje = date.today()
hoje = '{:%d-%m-%Y}'.format(hoje)

def ler_arquivo_csv(nome, pos=0):
    caminho = hoje + '/' + nome + '.csv'
    try:
        ficheiro = open(caminho, 'r')
        reader = csv.reader(ficheiro)
        precos = []
        for linha in reader:
                try:
                    precos.append(float(linha[pos]))
                except IndexError:
                    print('AÇÃO: ', nome)
                    return [False, None]
        ficheiro.close()
        return [True, precos]
    except FileNotFoundError:
        return [False, None]

def ler_arquivo_txt(nome_arquivo):
    arq = open(nome_arquivo + '.txt', 'r')
    texto = arq.readlines()
    acoes = texto
    arq.close()
    return acoes

def escrever_lista_em_txt(nome_arquivo, codigos):
    arq = open(nome_arquivo + '.txt', 'w')
    arq.writelines(codigos)
    arq.close
