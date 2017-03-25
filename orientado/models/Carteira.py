from .Acao import Acao
from .Mercado import Mercado
from utils import scrapper
from utils import data_utils
from utils import downloader
import operator
import plotly
import plotly.graph_objs as go


class Carteira(object):
    """A simple representation of a portfolio.

    :param mercado: A Mercado object, ...
    :param retorno_livre_risco: A float, ...
    :param tamanho: A int, ...
    :param acoes: A list of Acao objects, ...
    """

    def __init__(self, tamanho=10, mercado='IBOVESPA', metodo='RELAÇÃO'):
        self.mercado = Mercado(mercado)
        self.retorno_livre_risco = self.calcular_retorno_livre_risco()
        self.tamanho = tamanho
        self.acoes = self.mercado.acoes_mercado
        self.aplicar_metodo(metodo)


    def aplicar_metodo(self, metodo):
        if metodo == 'RELAÇÃO':
            tipo = 1
            self.acoes = self.calcular_relacao()
        self.montar_carteira(tipo)

    def montar_carteira(self, tipo):
        if tipo == 1:
            self.acoes.sort(key=operator.attrgetter('relacao'), reverse=True)
        self.acoes = self.acoes[:self.tamanho]

    def calcular_relacao(self):
        acoes_nao_descartadas = []
        tamanho_mercado = len(self.mercado.pontuacoes)
        for acao in self.acoes:

            retorno_requerido = acao.calcular_retorno_requerido(self.retorno_livre_risco, self.mercado)

            if retorno_requerido < acao.retorno_esperado and len(acao.retorno_diario) > 1:
                beta = acao.calcular_beta(self.mercado.retorno_diario)
                acao.relacao = acao.retorno_esperado/beta
                acoes_nao_descartadas.append(acao)
        return acoes_nao_descartadas

    def calcular_retorno_esperado(self):
        retorno_esperado = 0
        for acao in self.acoes:
            retorno_esperado += acao.retorno_esperado*(1/self.tamanho)
        return retorno_esperado

    def calcular_beta_carteira(self):
        beta = 0
        for acao in self.acoes:
            beta += acao.calcular_beta(self.mercado.retorno_diario)*(1/self.tamanho)
        return beta

    def calcular_retorno_livre_risco(self):
        arq = data_utils.get_arquivo('TAXA', 'SELIC', '.csv')
        taxa_percentual = data_utils.ler_arquivo_csv(arq)
        retorno_livre_risco = taxa_percentual[0]/100
        return retorno_livre_risco

    def mostrar_grafico(self):

        # Inicializa as variáveis que serão utilizadas na plotagem.
        retorno_esperado_acoes = []
        beta_acoes = []
        retorno_diario_mercado = self.mercado.retorno_diario
        codigo_acoes = []

        # Obtém os dados necessários.
        for acao in self.mercado.acoes_mercado:
            retorno_esperado_acoes.append(acao.retorno_esperado)
            beta = acao.calcular_beta(retorno_diario_mercado)
            beta_acoes.append(beta)
            codigo_acoes.append(acao.codigo)

        # Parte do gŕafico referente aos dados.
        data = [
            # Define a reta. Linha de Mercado de Títulos com (0, Rf) e (1, Rm).
            go.Scatter(
                x = [0, 1],
                y = [self.retorno_livre_risco, self.mercado.retorno_esperado],
                mode = 'lines',
                name = 'LMT'
            ),
            # Define os pontos. Ações com seus respectivos beta, Re, código.
            go.Scatter(
                x = beta_acoes,
                y = retorno_esperado_acoes,
                mode = 'markers',
                name = 'Ações',
                text = codigo_acoes
            )

        ]
        # Parte do gŕafico referente ao layout. (Titulo, Eixos, Grade)
        layout = go.Layout(
            title = 'Security Market Line',
            xaxis = dict(
                title = 'Beta'
            ),
            yaxis = dict(
                title = 'Retorno Esperado'
            )
        )

        # Monta a figura com as partes criadas, data e layout.
        fig = go.Figure(data=data, layout=layout)

        # Plota o gráfico num arquivo HTML e salva na pasta.
        plotly.offline.plot(fig, filename='teste.html')
