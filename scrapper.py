"""
OBJETIVO:   Gerar arquivo txt com os códigos das ações que compõe a carteira da
            IBOVESPA.
PASSOS:     1 - Acessar site da composição da carteira IBOVESPA.
            2 - Extrair os códigos das ações.
            3 - Salvar no arquivo 'AÇÕES_IBOVESPA.txt'
"""

# Contém as funções que manipulam arquivos.
import arquivos as arq
# Bilbioteca utilizada para capturar o conteúdo de uma página.
import requests
# Bilbioteca utilizada para fazer o scraping de uma página.
from bs4 import BeautifulSoup

def baixar_composicao_carteira_ibovespa():
    # Endereço da página onde encontram-se as ações que compôe a carteira IBOVESPA.
    html_carteira_ibovespa = 'http://www.bmfbovespa.com.br/pt_br/produtos/indices/indices-amplos/indice-ibovespa-ibovespa-composicao-da-carteira.htm'
    # Requisição do conteúdo da página.(page source)
    resposta_html = requests.get(html_carteira_ibovespa)
    # Analisa o conteúdo da página utilizando o html.parser.
    soup_html = BeautifulSoup(resposta_html.content, 'html.parser')

    # Procura o frame(JS) que contém os dados da carteira.
    frame_carteira = soup_html.find(id='bvmf_iframe')
    # Pega o endereço utlizado como fonte(src) desse script JS que monta o frame.
    url_carteira = frame_carteira['src']
    # Requisição do conteúdo do frame.(frame source)
    resposta_frame = requests.get(url_carteira)
    # Analisa o conteúdo do frame utilizando o html.parser.
    soup_frame = BeautifulSoup(resposta_frame.content, 'html.parser')

    # Procura todas as linhas onde há a tag 'td' com a classe 'rgSorted'. É onde
    # encontram-se os Códigos das ações.
    linhas_com_codigos = soup_frame.find_all('td', class_='rgSorted')
    # Iniciliza uma lista que vai conter as strings dos códigos. Ex: 'ABEV3\n'
    codigos = []
    # Para cada linha é retirada a string do código e adicionado uma quebra de linha.
    for linha in linhas_com_codigos:
        codigos.append(linha.contents[1].string + '\n')

    # Escreve a lista em um arquivo txt.
    arq.escrever_lista_em_txt('AÇÕES_IBOVESPA', codigos)
