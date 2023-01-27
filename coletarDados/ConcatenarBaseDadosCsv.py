import pandas
from ColetarDadosTwitter import ColetarDadosTwitter

class ConcatenarBaseDadosCsv:
    objColetarDados= ""
    listaCsv= []


    def __init__(self):
        self.objColetarDados= ColetarDadosTwitter()
        self.listaCsv.clear()


    def setObjColetarDados(self, valorObjColetarDados):
        self.objColetarDados= valorObjColetarDados


    def concatenarTodosCsv(self):
        anoLimite= self.objColetarDados.getAnoLimite()

        while(not int(self.objColetarDados.getAno()) > int(anoLimite)):
            try:
                print(self.objColetarDados.getPath() + '\\dados\\csv\\' + str(self.objColetarDados.getMes()) + '\\' + self.objColetarDados.getDtInicio() + self.objColetarDados.getNomeArqvCsv())
                with open(self.objColetarDados.getPath() + '\\dados\\csv\\' + str(self.objColetarDados.getMes()) + '\\' + self.objColetarDados.getDtInicio() + self.objColetarDados.getNomeArqvCsv(), "rb") as arqvCsv:
                    self.listaCsv.append(pandas.read_csv(arqvCsv))
                    arqvCsv.close()

                print('Concatenando .csv ' + self.objColetarDados.getDtInicio() + self.objColetarDados.getNomeArqvCsv() + '\n')
            except:
                print('Arquivo nao existe ' + self.objColetarDados.getDtInicio() + self.objColetarDados.getNomeArqvCsv() + '\n')
                self.objColetarDados.atualizarDatas()
                continue

            self.objColetarDados.atualizarDatas()

        csv_concatenado= pandas.concat(self.listaCsv, ignore_index=False)
        csv_concatenado.to_csv(self.objColetarDados.getPath() + '\\dados\\' + 'csv concatenado.csv', index = False)

        print('Base de dados salva em: ' + self.objColetarDados.getPath() + '\\dados\\' + 'csv concatenado.csv')
