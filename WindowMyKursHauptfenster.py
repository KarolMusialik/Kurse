import os
import PyQt5.uic as uic
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap, QIcon
import requests
from requests.auth import HTTPBasicAuth
from pathlib import Path
import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import WindowDiagramm
import mainMyPie

class WindowsMyKursHauptfenster:

    def __init__(self, initDict):
        self.isin = ''

        self.proxies = {
            "http": 'http://145.253.101.35:8888',
            "https": 'http://145.253.101.35:8888'
        }

        self.url = initDict.get('url_environment')
        self.workDir = initDict.get('workDir')
        self.user = 'diebayerische-cms'
        self.password = 'E@uo^NKEsa7pbW'
        self.sprache = ''  # --> in InvestorCountryList
        self.languageCode = ''  # --> in InvestorCountryList
        self.investorCountryCode = ''  # --> in InvestorCountryList
        self.investorTypeCode = ''  #--> in InvestorTypeList
        self.investorTypeName = ''  #--> in InvestorTypeList
        self.holdings = []
        self.holdingsDatum = ''
        self.industries = []
        self.industriesDatum = ''
        self.name = ''
        self.nav = 0
        self.navDate = ''
        self.wahrung = ''
        self.beginnDatum = ''

        self.distributionAppropriationDe = ''
        self.investorProfile = ''
        self.kvg = ''
        self.philosophyDe = ''

        self.anzahlDerEintraegeInGroesstePositionen = 10  # Anzahl der Einträge im Dialog


    def InitFenster(self, initDict):
        self.file_ui = initDict.get('file_MyKursHauptfenster')
        print(f'WindowsMyKursHauptfenster/__init__: die Infos zu dem Hauptfenster stehen in : {self.file_ui}')

        datei = Path(self.file_ui)
        if datei.is_file():
            print("WindowsMyKursHauptfenster/__init__:Datei " + self.file_ui + " existiert. Alles okay an dieser Stelle.")
            self.window = uic.loadUi(datei)

            self.window.pushButton_groesstePositionen.clicked.connect(self.RufeFensterGroesstePositionenAuf)

            self.fileGroesstePositionen = self.workDir + 'graph_groesstePosition.png'
            if Path(self.fileGroesstePositionen).is_file():
                os.remove(Path(self.fileGroesstePositionen))

            self.window.pushButton_groesstePositionenProzentual.clicked.connect(self.RufeFensterGroesstePositionenProzentualAuf)
            self.fileGroesstePositionenProzentual = self.workDir + 'graph_groesstePositionProzentual.png'
            if Path(self.fileGroesstePositionenProzentual).is_file():
                os.remove(Path(self.fileGroesstePositionenProzentual))

            self.window.pushButton_groessteBranche.clicked.connect(self.RufeFensterGroessteBrancheProzentualAuf)
            self.fileGroessteBranche = self.workDir + 'graph_groessteBranche.png'
            if Path(self.fileGroessteBranche).is_file():
                os.remove(Path(self.fileGroessteBranche))

            self.window.pushButton_groessteBrancheProzentual.clicked.connect(self.RufeFensterGroessteBrancheAuf)
            self.fileGroessteBrancheProzentual = self.workDir + 'graph_groessteBrancheProzentual.png'
            if Path(self.fileGroessteBrancheProzentual).is_file():
                os.remove(Path(self.fileGroessteBrancheProzentual))

        else:
            print("indowsMyKursHauptfenster/__init__:Datei " + self.file_ui + " existiert nicht!!!. Das fuehrt zum Programmabbruch!")
            self.window = None


    def RufeFensterGroesstePositionenAuf(self):
        paramDict = {}
        paramDict['file'] = self.fileGroesstePositionen
        paramDict['workDir'] = self.workDir
        self.ZeigeDiagrammImNeuenFenster(paramDict)

    def RufeFensterGroesstePositionenProzentualAuf(self):
        paramDict = {}
        paramDict['file'] = self.fileGroesstePositionenProzentual
        paramDict['workDir'] = self.workDir
        self.ZeigeDiagrammImNeuenFenster(paramDict)

    def RufeFensterGroessteBrancheAuf(self):
        paramDict = {}
        paramDict['file'] = self.fileGroessteBranche
        paramDict['workDir'] = self.workDir
        self.ZeigeDiagrammImNeuenFenster(paramDict)

    def RufeFensterGroessteBrancheProzentualAuf(self):
        paramDict = {}
        paramDict['file'] = self.fileGroessteBrancheProzentual
        paramDict['workDir'] = self.workDir
        self.ZeigeDiagrammImNeuenFenster(paramDict)

    def ZeigeDiagrammImNeuenFenster(self, paramDict):
        ow = WindowDiagramm.WindowDiagrammm(paramDict)
    def PercentageToFloat(self, wertStr):
        if wertStr == None:
            return 0.0

        wert_str = wertStr.replace('%', '')
        wert_float = self.StringToFloat(wert_str)

        return wert_float/100.0

    def StringToFloat(self, wertStr):

        if wertStr == None:
            return 0.0

        wert_str = wertStr.replace('.', '')
        wert_str = wert_str.replace(',', '.')
        return float(wert_str)

    def GetListeAllerFonds(self):
        #Die Liste wird aus den evaluated Parameter Combinations erzeugt:
        liste = []  # zuerst ist sie leer

        # jetzt wird der Webserver gelesen. Als Antwort w
        url = self.url + '/api/evaluatedParameterCombinations/'
        resp = requests.get(url, proxies=self.proxies, auth=HTTPBasicAuth(self.user, self.password))
        print('GetListeAllerFonds: --- Beginn: ---')
        print(resp.status_code)
        print(resp.content)

        tempJson1 = json.loads(resp.text)  # Umwandlung von String  zu Json also Dict
        if len(tempJson1) == 0:
            print('GetListeAllerFonds: keine Produktdaten vorhanden. --> Abbruch!')
            print('GetListeAllerFonds: --- Ende ---:')
            return

        for x, y in tempJson1.items():
            isin = y.get('isin')
            prodactData = self.ProductData(isin)
            eintrag = isin + '_' + prodactData.get('name')
            liste.append(eintrag)

        print('GetListeAllerFonds: --- Ende ---:')
        return liste

    def SchliesseFenster(self):
        self.window.close()

    def zeigeFenster(self):
        self.window.pushButton_Weiter.clicked.connect(self.SchliesseFenster)

        self.window.label_isin_wert.setText(self.isin)
        self.window.label_name_wert.setText(self.name)
        self.window.label_nav_wert.setText(str(self.nav))
        self.window.label_navDate_wert.setText(str(self.navDate))
        self.window.label_BeginnDatum_wert.setText(str(self.beginnDatum))
        self.window.label_waehrung_wert.setText(str(self.wahrung))

        self.window.label_DistributionAppropriationDe.setText(str(self.distributionAppropriationDe))
        self.window.label_investorProfile.setText(str(self.investorProfile))
        self.window.label_KVG.setText(str(self.kvg))
        self.window.label_philosophyDe.setText(str(self.philosophyDe))


        self.BelegePortfolioGroestePositionen()
        self.BelegePortfolioGroesteBranchen()

        self.window.exec_()

    def BelegePortfolioGroestePositionen(self):

        self.window.label_holdingsDatum_wert.setText(self.holdingsDatum)
        layout = self.window.gridLayout_Positionen

        label1 = QLabel('Name')
        label2 = QLabel('Anteil')
        label3 = QLabel('absoluter Wert')
        layout.addWidget(label1, 0, 0)
        layout.addWidget(label2, 0, 1)
        layout.addWidget(label3, 0, 2)

        i = 1

        labels = []
        percentage = []
        absoluteValue = []

        for wert in self.holdings:

            name = wert.get('title')
            labels.append(name)

            anteil = wert.get('percentage')
            wert_float = self.PercentageToFloat(anteil)
            percentage.append(wert_float)

            wertAnsolut = wert.get('absoluteValue')
            wert_float = self.StringToFloat(wertAnsolut)
            absoluteValue.append(wert_float)

            label1 = QLabel(str(name))
            label2 = QLabel(str(anteil))
            label3 = QLabel(str(wertAnsolut))

            layout.addWidget(label1, i, 0)
            layout.addWidget(label2, i, 1)
            layout.addWidget(label3, i, 2)
            i = i + 1

        #jetzt wird ein Graph gezeichnet:
        title = 'absolute Verteilung'
        sizes = absoluteValue
        paramDict = {}
        if self.PruefeSizes(sizes) == 0:
            fileSource = self.workDir + 'LeereBox.png'
            fileDestination = self.fileGroesstePositionen

            os.system('copy ' + fileSource + ' ' + fileDestination)
            file = self.fileGroesstePositionen

        else:
            paramDict['title'] = title
            paramDict['sizes'] = sizes
            paramDict['labels'] = labels
            file = self.fileGroesstePositionen
            paramDict['file'] = file
            mainMyPie.ZeichnePie(paramDict)

        #jetzt wird der Graph(*.png) in das Dialog gesetzt:
        paramDict.clear()
        paramDict['file'] = file
        paramDict['pushButton'] = self.window.pushButton_groesstePositionen
        self.SetzeDiagrammInDialog(paramDict)

        #jetzt wird ein Graph gezeichnet:
        title = 'prozentuale Verteilung'
        sizes = percentage
        paramDict = {}
        if self.PruefeSizes(sizes) == 0:
            fileSource = self.workDir + 'LeereBox.png'
            fileDestination = self.fileGroesstePositionenProzentual

            os.system('copy ' + fileSource + ' ' + fileDestination)
            file = self.fileGroesstePositionenProzentual

        else:
            paramDict['title'] = title
            paramDict['sizes'] = sizes
            paramDict['labels'] = labels
            file = self.fileGroesstePositionenProzentual
            paramDict['file'] = file
            mainMyPie.ZeichnePie(paramDict)

        #jetzt wird der Graph(*.png) in das Dialog gesetzt:
        paramDict.clear()
        paramDict['file'] = file
        paramDict['pushButton'] = self.window.pushButton_groesstePositionenProzentual
        self.SetzeDiagrammInDialog(paramDict)


    def PruefeSizes(self, sizes):
        sum = 0.0
        for x in sizes:
            sum = sum + float(x)

        return sum

    def SetzeDiagrammInDialog(self, paramDict):
        file = paramDict.get('file')
        if file is None:
            print('SetzeDiagrammInDialog: keine Datei vorhanden. Fehler!')
            return 1

        pushButton = paramDict.get('pushButton')
        if pushButton is None:
            print('SetzeDiagrammInDialog: kein Pushbuttom mit dem Namen vorhanden. Fehler!')
            return 1

        # jetzt wird der Graph(*.png) in das Dialog gesetzt:
        size = pushButton.size()
        pushButton.setIcon(QIcon(file))
        pushButton.setIconSize(size)

    def BelegePortfolioGroesteBranchen(self):

        self.window.label_industriesDatum_wert.setText(self.industriesDatum)

        layout = self.window.gridLayout_Branchen

        label1 = QLabel('Name')
        label2 = QLabel('Anteil')
        label3 = QLabel('absoluter Wert')
        layout.addWidget(label1, 0, 0)
        layout.addWidget(label2, 0, 1)
        layout.addWidget(label3, 0, 2)

        i = 1

        labels = []
        percentage = []
        absoluteValue = []

        for wert in self.industries:

            name = wert.get('title')
            labels.append(name)

            anteil = wert.get('percentage')
            wert_float = self.PercentageToFloat(anteil)
            percentage.append(wert_float)

            wertAbsolut = wert.get('absoluteValue')
            wert_float = self.StringToFloat(wertAbsolut)
            absoluteValue.append(wert_float)

            label1 = QLabel(str(name))
            label2 = QLabel(str(anteil))
            label3 = QLabel(str(wertAbsolut))

            layout.addWidget(label1, i, 0)
            layout.addWidget(label2, i, 1)
            layout.addWidget(label3, i, 2)
            i = i + 1

        # jetzt wird ein Graph gezeichnet:
        title = 'absolute Aufteilung'
        sizes = absoluteValue
        paramDict = {}
        if self.PruefeSizes(sizes) == 0:
            fileSource = self.workDir + 'LeereBox.png'
            fileDestination = self.fileGroessteBranche

            os.system('copy ' + fileSource + ' ' + fileDestination)
            file = self.fileGroessteBranche

        else:
            paramDict['title'] = title
            paramDict['sizes'] = sizes
            paramDict['labels'] = labels
            file = self.fileGroessteBranche
            paramDict['file'] = file
            mainMyPie.ZeichnePie(paramDict)

        # jetzt wird der Graph(*.png) in das Dialog gesetzt:
        paramDict.clear()
        paramDict['file'] = file
        paramDict['pushButton'] = self.window.pushButton_groessteBranche
        self.SetzeDiagrammInDialog(paramDict)

        # jetzt wird ein Graph gezeichnet:
        title = 'prozentuale Aufteilung'
        sizes = percentage
        paramDict = {}
        if self.PruefeSizes(sizes) == 0:
            fileSource = self.workDir + 'LeereBox.png'
            fileDestination = self.fileGroessteBrancheProzentual

            os.system('copy ' + fileSource + ' ' + fileDestination)
            file = self.fileGroessteBrancheProzentual

        else:
            paramDict['title'] = title
            paramDict['sizes'] = sizes
            paramDict['labels'] = labels
            file = self.fileGroessteBrancheProzentual
            paramDict['file'] = file
            mainMyPie.ZeichnePie(paramDict)

        # jetzt wird der Graph(*.png) in das Dialog gesetzt:
        paramDict.clear()
        paramDict['file'] = file
        paramDict['pushButton'] = self.window.pushButton_groessteBrancheProzentual
        self.SetzeDiagrammInDialog(paramDict)

    def InvestorTypeList(self):

        url = self.url + '/api/investorTypeList/'
        resp = requests.get(url, proxies=self.proxies, auth=HTTPBasicAuth(self.user, self.password))
        print('InvestorTypeList: --- Beginn: ---')
        print(resp.status_code)
        print(resp.content)

        tempJson1 = json.loads(resp.text)  # Umwandlung von String  zu Json also Dict
        if len(tempJson1) == 0:
            print('InvestorTypeList: keine Produktdaten vorhanden. --> Abbruch!')
            print('InvestorTypeList: --- Ende ---:')
            return

        tempJson2 = tempJson1.get('global')
        print(f'InvestorTypeList: {tempJson2}')
        self.investorTypeCode = tempJson2.get('code')
        self.investorTypeName = tempJson2.get('name')

        print('InvestorTypeList: --- Ende ---:')

    def InvestorCountryList(self):

        url = self.url + '/api/investorCountryList/'
        resp = requests.get(url, proxies=self.proxies, auth=HTTPBasicAuth(self.user, self.password))
        print('InvestorCountryList: --- Beginn: ---')
        print(resp.status_code)
        print(resp.content)

        tempJson1 = json.loads(resp.text)  # Umwandlung von String  zu Json also Dict
        if len(tempJson1) == 0:
            print('InvestorCountryList: keine Produktdaten vorhanden. --> Abbruch!')
            print('InvestorCountryList: --- Ende ---:')
            return

        tempJson2 = tempJson1.get('de')
        print(f'InvestorCountryList: {tempJson2}')
        self.languageCode = tempJson2.get('code')
        self.sprache = tempJson2.get('code')
        self.investorCountryCode = tempJson2.get('code')

        print('InvestorCountryList: --- Ende ---:')

    def EvaluatedPageList(self):
        url = self.url + '/api/evaluatedPageList/' + str(self.isin) + '/'
        resp = requests.get(url, proxies=self.proxies, auth=HTTPBasicAuth(self.user, self.password))
        print('EvaluatedPageList: --- Beginn: ---')
        print(resp.status_code)
        print(resp.content)
        print('EvaluatedPageList: --- Ende ---:')

    def EvaluatedParameterCombinations(self):
        url = self.url + '/api/evaluatedParameterCombinations/'
        resp = requests.get(url, proxies=self.proxies, auth=HTTPBasicAuth(self.user, self.password))
        print('EvaluatedParameterCombinations: --- Beginn: ---')
        print(resp.status_code)
        print(resp.content)
        print('EvaluatedParameterCombinations: --- Ende ---:')

    def ProductList(self):
        url = self.url + '/api/productList/'
        resp = requests.get(url, proxies=self.proxies, auth=HTTPBasicAuth(self.user, self.password))
        print('ProductList: --- Beginn: ---')
        print(resp.status_code)
        print(resp.content)

        tempJson1 = json.loads(resp.text)  # Umwandlung von String  zu Json also Dict

        if len(tempJson1) == 0:
            print('ProductList: keine Produktdaten vorhanden. --> Abbruch!')
            print('ProductList: --- Ende ---:')
            return

        # jetzt werden die Daten zu den Holdings rausgeholt:
        tempJson2 = tempJson1.get(self.isin)
        print(tempJson2)
        self.distributionAppropriationDe = tempJson2.get('distributionAppropriationDe')
        self.investorProfile = tempJson2.get('investorProfile')
        self.kvg = tempJson2.get('kvg')
        self.philosophyDe = tempJson2.get('philosophyDe')

        print('ProductList: --- Ende ---:')

    def LeseInfosZuIsin(self, isinInfosDict):
        url = self.url + '/api/productList/'
        resp = requests.get(url, proxies=self.proxies, auth=HTTPBasicAuth(self.user, self.password))
        print('LeseInfosZuIsin: --- Beginn: ---')
        print(resp.status_code)
        #print(resp.content)

        tempJson1 = json.loads(resp.text)  # Umwandlung von String  zu Json also Dict

        if len(tempJson1) == 0:
            print('LeseInfosZuIsin: keine Produktdaten vorhanden. --> Abbruch!')
            print('LeseInfosZuIsin: --- Ende ---:')
            return

        isin = isinInfosDict.get('isin')
        # jetzt werden die Daten zu isin eingeschränkt:
        tempJson2 = tempJson1.get(isin)
        print(tempJson2)
        if len(tempJson2) == 0:
            print('LeseInfosZuIsin: keine Produktdaten vorhanden. --> Abbruch!')
            print('LeseInfosZuIsin: --- Ende ---:')
            return

        isinInfosDict['name'] = tempJson2.get('name')
        isinInfosDict['nav'] = tempJson2.get('nav')
        isinInfosDict['navDate'] = tempJson2.get('navDate')
        isinInfosDict['currencyCode'] = tempJson2.get('currencyCode')
        isinInfosDict['inceptionDate'] = tempJson2.get('inceptionDate')
        isinInfosDict['distributionAppropriationDe'] = tempJson2.get('distributionAppropriationDe')
        isinInfosDict['investorProfile'] = tempJson2.get('investorProfile')
        isinInfosDict['kvg'] = tempJson2.get('kvg')
        isinInfosDict['philosophyDe'] = tempJson2.get('philosophyDe')

        print('LeseInfosZuIsin: --- Ende ---:')

    def PageList(self):
        url = self.url + '/api/pageList/'
        resp = requests.get(url, proxies=self.proxies, auth=HTTPBasicAuth(self.user, self.password))
        print('PageList: --- Beginn: ---')
        print(resp.status_code)
        print(resp.content)
        print('PageList: --- Ende ---:')

    def ProductData(self, isin):
        url = self.url + '/api/productData/' + str(isin) + '/'
        resp = requests.get(url, proxies=self.proxies, auth=HTTPBasicAuth(self.user, self.password))

        print('ProductData: --- Beginn: ---')
        print(resp.status_code)
        print(resp.text)

        tempJson1 = json.loads(resp.text)  # Umwandlung von String  zu Json also Dict

        if len(tempJson1) == 0:
            print('ProductData: keine Produktdaten vorhanden. --> Abbruch!')
            print('ProductData: --- Ende ---:')
            return


        # jetzt werden die Daten zu den Holdings rausgeholt:
        tempJson2 = tempJson1.get(isin)
        #print(tempJson2)
        self.name = tempJson2.get('name')
        self.nav = tempJson2.get('nav')
        self.navDate = tempJson2.get('navDate')
        self.wahrung = tempJson2.get('currencyCode')
        self.beginnDatum = tempJson2.get('inceptionDate')

        print('ProductData: --- Ende ---:')
        return tempJson2

    def HistoricPriceData(self):
        url = self.url + '/api/historicPriceData/' + str(self.isin) +'/' + str(self.sprache) +'/'

        resp = requests.get(url, proxies=self.proxies, auth=HTTPBasicAuth(self.user, self.password))
        print('HistoricPriceDate: --- Beginn: ---')
        print(resp.status_code)
        print(resp.text)

        if resp.status_code != 200:
            print(f'HistoricPriceData: keine Antwort vom Webservice. --> keine Daten aus dieser Funktion!')
            return

        tempJson1 = json.loads(resp.text)  # Umwandlung von String  zu Json also Dict

        if len(tempJson1) == 0:
            print('HistoricPriceData: keine Produktdaten vorhanden. --> keine Daten aus dieser Funktion!')
            return

        navDate = []
        currencyCode = []
        nav = []
        navChange = []
        navChangePercent = []

        for datum, wertDict in tempJson1.items():
            date_object = datetime.strptime(wertDict.get('navDate'), '%d.%m.%Y').date()
            navDate.append(date_object)
            currencyCode.append(wertDict.get('currencyCode'))

            wert_str = wertDict.get('nav')
            wert_float = self.StringToFloat(wert_str)
            nav.append(wert_float)

            wert_str = wertDict.get('navChange')
            wert_float = self.StringToFloat(wert_str)
            navChange.append(wert_float)

            wert_str = wertDict.get('navChangePercent')
            wert_float = self.PercentageToFloat(wert_str)
            navChangePercent.append(wert_float)

        data = {'navDate': navDate, 'currencyCode': currencyCode, 'nav': nav, 'navChange': navChange, 'navChangePercent': navChangePercent}
        df = pd.DataFrame(data)
        df.plot(x='navDate', y='nav', title='Fondsentwicklung')
        #plt.show()
        plt.savefig('graph_nav')

        pixmap = QPixmap('graph_nav.png')
        self.window.label_nav.setPixmap(pixmap)
        self.window.label_nav.resize(pixmap.width(), pixmap.height())

        df.plot(x='navDate', y='navChangePercent', title='Fondsveränderung')
        #plt.show()
        plt.savefig('graph_navChangePercent')

        pixmap = QPixmap('graph_navChangePercent.png')
        self.window.label_percentage.setPixmap(pixmap)

        self.window.label_percentage.resize(pixmap.width(), pixmap.height())

        print('HistoricPriceDate: --- Ende ---:')

    def Documents(self):
        url = self.url + '/api/documents/' + str(self.isin) + '/' + self.investorCountryCode + '/' + self.investorTypeCode + '/' + self.languageCode + '/'

        resp = requests.get(url, proxies=self.proxies, auth=HTTPBasicAuth(self.user, self.password))
        print('Documents: --- Beginn: ---')
        print(resp.status_code)
        if resp.status_code != 200:
            print('Documents: keine Antwort vom Webservice. Abbruch!')
            return

        print(resp.text)


        print('Documents: --- Ende ---:')


    def AllocationDate(self):
        url = self.url + '/api/allocationData/' + str(self.isin) +'/'+ str(self.sprache) +'/'
        resp = requests.get(url, proxies=self.proxies, auth=HTTPBasicAuth(self.user, self.password))
        print('AllocationDate: --- Beginn: ---')
        print(resp.status_code)
        print(resp.text)
        tempJson1 = json.loads(resp.text)  # Umwandlung von String  zu Json also Dict

        if len(tempJson1) == 0:
            print('AllocationDate: keine Produktdaten vorhanden. --> Abbruch!')
            print('AllocationDate: --- Ende ---:')
            return


        # jetzt werden die Daten zu den Holdings rausgeholt:
        tempJson2 = tempJson1.get('holdings')
        if tempJson2 == None:
            self.holdings = []
            self.holdingsDatum = ''
        else:
            tempListe = tempJson2.get('values')
            self.holdings = tempListe
            self.holdingsDatum = tempJson2.get('date')
            print(f'holdings: {self.holdings} und Datum {self.holdingsDatum}')

        # jetzt werden die Daten zu den indistries rausgeholt:
        tempJson2 = tempJson1.get('industries')
        if tempJson2 == None:
            self.industries = []
            self.industriesDatum = ''
        else:
            tempListe = tempJson2.get('values')
            self.industries = tempListe
            self.industriesDatum = tempJson2.get('date')

            print(f'industries: {self.industries} und Datum {self.industriesDatum}')

        print('AllocationDate: --- Ende ---:')










