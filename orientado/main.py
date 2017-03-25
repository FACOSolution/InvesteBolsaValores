from models.Carteira import Carteira
from models.Acao import Acao
from models.Mercado import Mercado

portfolio = Carteira()

print('\n\tAÇÕES IBOVESPA..........: ', len(portfolio.mercado.acoes_mercado))
#print('\tAÇÕES AVALIADAS.........: ', qtd_avaliada)
print('\tAÇÕES NÃO DESCARTADAS...: ', len(portfolio.acoes))
print('\tAÇÕES DA CARTEIRA.......: ', portfolio.tamanho)
print('\n\t\tCOMPOSIÇÃO\n\tAÇÃO\tRELAÇÃO (RE/BETA)\n')

for acao in portfolio.acoes:
    print('\t%s\t%f' % (acao.codigo, acao.relacao))

print('\nRetorno Esperado da Carteira em % : ', portfolio.calcular_retorno_esperado()*100)
print('Beta da Carteira : ', portfolio.calcular_beta_carteira())

portfolio.mostrar_grafico()
