import csv
from datetime import date
from os.path import join

hoje = date.today()
hoje = '{:%d-%m-%Y}'.format(hoje)

# caminho = hoje + '/' + nome + '.csv'
caminho = 'datasets'

def ler_arquivo_csv(nome, pos=0):
    precos = []
    try:
        ficheiro = open(join(caminho, nome + '.csv'), 'r')
        reader = csv.reader(ficheiro)

        for linha in reader:
            precos.append(float(linha[pos]))
        ficheiro.close()
    except:
        #print('Não foi possível abrir o arquivo ')
        pass
    return precos

def escrever_csv(nome_arquivo, dados, index=False, header=False):
    dados.to_csv(join(caminho, nome_arquivo + '.csv'), index=index, header=header)



def ler_arquivo_txt(nome_arquivo):
    acoes = []
    try:
        arq = open(join(caminho, nome_arquivo + '.txt'), 'r')
        for linha in arq:
            acoes.append(linha[0:-1])
        arq.close()
    except:
        pass
    return acoes

def escrever_lista_em_txt(nome_arquivo, codigos):
    arq = open(join(caminho, nome_arquivo + '.txt'), 'w')
    novo = []
    for codigo in codigos:
        codigo = codigo + '\n'
        novo.append(codigo)
    arq.writelines(novo)
    arq.close

def converter_recArray_para_list(recArray, column_name):
    ndArray = recArray[column_name]
    lista = ndArray.tolist()
    return lista
