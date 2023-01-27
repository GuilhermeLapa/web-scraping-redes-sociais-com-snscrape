import pandas
import os
import json
import time
import shutil
import snscrape.modules.twitter as sntwitter

class ColetarDadosTwitter:
    path= ""
    nomeArqvJson= ""
    nomeArqvCsv= ""
    dtInicio= ""
    dtFim= ""
    termoBusca= ""
    linguagem= ""
    ano= 1
    mes= 1
    qtdDiasIncrementar= 1
    mesAnterior= ""
    anoLimite= 1
    qtdLimiteTweets= 0


    def __init__(self):
        self.path = os.getcwd()
        self.nomeArqvJson= "dadosJson.json"
        self.nomeArqvCsv= "dadosCsv.csv"
        self.ano= 1
        self.mes= 1
        self.anoLimite= 1
        self.qtdDiasIncrementar= 1


    def setDtInicio(self, valorDtInicio):
        self.dtInicio= valorDtInicio
        self.anoLimite= self.dtInicio[0:4]

    def getDtInicio(self):
        return self.dtInicio


    def setDtFim(self, valorDtFim):
        self.dtFim= valorDtFim
        self.mesAnterior= self.dtFim[5:7]

    def getDtFim(self):
        return self.dtFim


    def getNomeArqvJson(self):
        return self.nomeArqvJson

    def getNomeArqvCsv(self):
        return self.nomeArqvCsv


    def setTermoBusca(self, valorTermoBusca):
        self.termoBusca= valorTermoBusca


    def setLinguagem(self, valorLinguagem):
        self.linguagem= valorLinguagem


    def setQtdDiasIncrementar(self, valorQtdDiasIncrementar):
        self.qtdDiasIncrementar= valorQtdDiasIncrementar

    def getQtdDiasIncrementar(self):
        return self.qtdDiasIncrementar


    def setQtdLimiteTweets(self, valorQtdLimiteTweets):
        self.qtdLimiteTweets= valorQtdLimiteTweets

    def getAnoLimite(self):
        return self.anoLimite

    def getPath(self):
        return self.path

    def getAno(self):
        return self.ano

    def getMes(self):
        return self.mes


    def criarEstruturaPastas(self):
        pastaMes= 1
        pastaDados= os.getcwd() + '\\dados'
        pastaCsv= os.getcwd() + '\\dados\\csv'
        pastaJson= os.getcwd() + '\\dados\\json'

        if(not os.path.exists(pastaDados)):
            #Pasta dados
            os.mkdir(pastaDados)

        if(not os.path.exists(pastaCsv)):
            #Pasta csv
            os.mkdir(pastaCsv)

        if(not os.path.exists(pastaJson)):
            #Pasta json
            os.mkdir(pastaJson)

        while(not int(pastaMes) > 12):
            try:
                if(not os.path.exists(pastaCsv + '\\' + str(pastaMes))):
                    os.mkdir(pastaCsv + '\\' + str(pastaMes))

                if(not os.path.exists(pastaJson + '\\' + str(pastaMes))):
                    os.mkdir(pastaJson + '\\' + str(pastaMes))
            except:
                print('Erro ao criar pasta: ' + pastaMes)

            pastaMes= pastaMes + 1


    def deletarEstruturaPastas(self):
        shutil.rmtree(os.getcwd() + '\\dados')


    def existeEstruturaPastas(self):
        resultado= False

        if(os.path.exists(os.getcwd() + '\\dados')):
            resultado= True
        
        return resultado

    
    def incrementarDias(self, data, qtdDias):
        ano= int(data[0:4])
        mes= int(data[5:7])
        dia= int(data[8:10])

        meses1= [1,3,5,7,8,10,12]
        meses2= [4,6,9,11]

        if(mes in meses1):
            #ate dia 31
            if((dia + qtdDias) > 31):
                mes= mes + 1
                dia= (dia + qtdDias) - 31
            else:
                dia= dia + qtdDias
        elif(mes == 2):
            #ate dia 28
            if((dia + qtdDias) > 28):
                mes= mes + 1
                dia= (dia + qtdDias) - 28
            else:
                dia= dia + qtdDias
        elif(mes in meses2):
            if((dia + qtdDias) > 30):
                mes= mes + 1
                dia= (dia + qtdDias) - 30
            else:
                dia= dia + qtdDias

        if(mes > 12):
            ano= ano + 1
            mes= 1

        aux= [1,2,3,4,5,6,7,8,9]
        if(dia in aux):
            dia= "0" + str(dia)

        if(mes in aux):
            mes= "0" + str(mes)

        resultado= str(ano) + "-" + str(mes) + "-" + str(dia)

        return resultado


    def atualizarDatas(self):
        self.setDtInicio(self.incrementarDias(self.dtFim, self.qtdDiasIncrementar))
        self.setDtFim(self.incrementarDias(self.dtInicio, self.qtdDiasIncrementar))
        self.ano= int(self.dtFim[0:4])
        self.mes= int(self.dtFim[5:7])

        if(int(self.mes) > int(self.mesAnterior)):
            self.mesAnterior= int(self.mes)


    def executarColetaPorAno(self):
        while(not int(self.ano) > int(self.anoLimite)):    
            print("Obtendo Tweets do periodo: " + self.dtInicio + " ate " + self.dtFim)

            ################################SNSCRAPE#################################
            query= "\""+self.termoBusca+"\" lang:"+self.linguagem+" min_replies:0 min_faves:0 min_retweets:0 until:"+self.dtFim+" since:"+self.dtInicio
            print('Consulta: ' + query)

            listaTweets= []
            limite= self.qtdLimiteTweets

            for tweet in sntwitter.TwitterSearchScraper(query).get_items():
                auxDict= {"id": tweet.id, "date": str(tweet.date)[0:19], "rawContent": tweet.rawContent, "likeCount": tweet.likeCount, "userId": tweet.user.id, "userName":  tweet.user.username, "userVerified":  tweet.user.verified, "userLocation": tweet.user.location}
                listaTweets.append(auxDict)
                if len(listaTweets) >= limite:
                    break
            ################################SNSCRAPE#################################

            try:
                #salvar em um arquivo .json
                arqvJson= open(self.path + '\\dados\\json\\'+str(self.mes)+'\\' + self.dtInicio + self.nomeArqvJson, "a")
                json.dump(listaTweets, arqvJson)
                arqvJson.close()
                print('Criando .json ' + self.dtInicio + self.nomeArqvJson + '\n')
            except:
                print('Erro ao criar arquivo .json: ' + self.dtInicio + self.nomeArqvJson + '\n')
                self.atualizarDatas()
                continue

            listaTweets.clear()

            self.atualizarDatas()
            time.sleep(1)


    def salvarDoJsonEmCsv(self):
        self.ano= 1
        self.mes= 1

        while(not int(self.ano) > int(self.anoLimite)):
            try:
                with open(self.path + '\\dados\\json\\'+str(self.mes)+'\\' + self.dtInicio + self.nomeArqvJson, "r") as arqvJson:
                    df= pandas.read_json(arqvJson)
                    arqvJson.close()

                df.to_csv(self.path + '\\dados\\csv\\'+str(self.mes)+'\\' + self.dtInicio + self.nomeArqvCsv, index = False)

                print('Criando .csv ' + self.dtInicio + self.nomeArqvJson + '\n')
            except:
                print('Arquivo nao existe ' + self.dtInicio + self.nomeArqvJson + '\n')
                self.atualizarDatas()
                    
                continue

            self.atualizarDatas()
