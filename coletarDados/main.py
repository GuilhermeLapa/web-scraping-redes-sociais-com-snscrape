from ColetarDadosTwitter import ColetarDadosTwitter
from ConcatenarBaseDadosCsv import ConcatenarBaseDadosCsv

dtInicio= "2020-01-01"
dtFim= "2020-01-02"
termoBusca= "termoBusca"
linguagem= "pt"
periodoEntreDias= 1
qtdLimiteTweets= 5000

#Coleta de dados
coletarDados= ColetarDadosTwitter()

if(coletarDados.existeEstruturaPastas()):
    coletarDados.deletarEstruturaPastas()
coletarDados.criarEstruturaPastas()

coletarDados.setDtInicio(dtInicio)
coletarDados.setDtFim(dtFim)
coletarDados.setTermoBusca(termoBusca)
coletarDados.setLinguagem(linguagem)
coletarDados.setQtdDiasIncrementar(periodoEntreDias)
coletarDados.setQtdLimiteTweets(qtdLimiteTweets)

coletarDados.executarColetaPorAno()

coletarDados.setDtInicio(dtInicio)
coletarDados.setDtFim(dtFim)
coletarDados.salvarDoJsonEmCsv()

#Gerar base de dados
coletarDados= None
coletarDados= ColetarDadosTwitter()
concatenarBase= ConcatenarBaseDadosCsv()
concatenarBase.setObjColetarDados(coletarDados)
concatenarBase.objColetarDados.setDtInicio(dtInicio)
concatenarBase.objColetarDados.setDtFim(dtFim)
concatenarBase.concatenarTodosCsv()
