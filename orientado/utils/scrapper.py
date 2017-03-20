import requests
from bs4 import BeautifulSoup

def baixar_composicao_carteira_ibovespa():
    html = 'http://bvmf.bmfbovespa.com.br/indices' \
            + '/ResumoCarteiraTeorica.aspx?Indice=IBOV&idioma=pt-br'
    resposta_html = requests.get(html)
    soup = BeautifulSoup(resposta_html.content, 'html.parser')
    linhas_com_codigos = soup.find_all('td', class_='rgSorted')
    codigos = []
    for linha in linhas_com_codigos:
        codigos.append(linha.contents[1].string)

    return codigos
