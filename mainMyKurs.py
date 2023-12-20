import sys
import myKurs
from PyQt5 import QtWidgets
import PyQt5.uic as uic
from PyQt5.QtWidgets import QMessageBox
import pandas as pd
from pathlib import Path
import datetime

import einstellung
import protokoll


def SchliesseFenster():
    owindow.close()

def LeseFondsliste():
    datei = parameterDict.get('file_Fondsliste')
    datei_path = Path(datei)

    print('LeseFondsliste: --- Beginn ---')
    if datei_path.is_file():
        print(f'LeseFondsliste: Datei {datei} existiert. Alles okay.')
    else:
        print(f'LeseFondsliste: Datei {datei} existiert nicht. Fehler! Abbruch')
        sys.exit()

    f = open(datei, 'r')  # Datei wird nur zum Lesen eröffnet

    aktuelleFondsliste.clear()  # aktuelle Liste der Fonds wird gelöscht

    for row in f:
        eintrag = row[:-2]
        aktuelleFondsliste.append(eintrag)

    SchreibeAktuelleListeInComboBox()

    owindow.comboBox_Fondsliste.currentTextChanged.connect(WechselDesEintrags)
    f.close()
    print('LeseFondsliste: --- Ende ---')


def BelegeNeueFondslisteWegenFilter(s):

    anzahl = len(aktuelleFondsliste)
    i = 0
    neueListe = []

    while i < anzahl:
        eintrag = aktuelleFondsliste[i]
        if s in eintrag:  # falls der Filterwert in der Liste erhalten ist, dann bleibt der Listeneintrag
            neueListe.append(eintrag)

        i += 1

    anzahl = len(neueListe)
    i = 0
    aktuelleFondsliste.clear()
    while i < anzahl:
        eintrag = neueListe[i]
        aktuelleFondsliste.append(eintrag)
        i += 1


def SchreibeAktuelleListeInComboBox():
    anzahl = len(aktuelleFondsliste)
    i = 0
    owindow.comboBox_Fondsliste.clear()
    while i < anzahl:
        eintrag = aktuelleFondsliste[i]
        owindow.comboBox_Fondsliste.addItem(eintrag)
        i += 1


def FilterEintragChanged():

    s = owindow.lineEdit_FilterFonds.text()
    if s == '':
        LeseFondsliste()
    else:
        BelegeNeueFondslisteWegenFilter(s)

    SchreibeAktuelleListeInComboBox()


def LeseIsinAusEintrag(s):
    anzahl = len(s)
    if anzahl == 0:
        isin = ''
        return isin

    isin = ''
    i = 0
    while i <= anzahl:
        if s[i] == '_':  #das Trennzeichen wurde erreicht
            return isin
        else:
            isin = isin + s[i]

        i += 1

    print('LeseIsinAusEintrag: Fehler, weil kein Trennzeichen entdeckt wurde. Damit wurde keine isin ermittelt. Der Text lautetet.' +s)


def WechselDesEintrags(s):
    print('LeseisinAusEintrag: neuer Wert: '+ s)
    isin = LeseIsinAusEintrag(s)
    owindow.textEdit_isin.setText(isin)


def GetClickedCell(row, column):

    isin = owindow.tableWidget_Fondsliste.item(row, 0).text()
    owindow.textEdit_isin.setText(isin)

    print('clicked!', isin)

def DialogDateiAuswahlen():
    ergebnis = QtWidgets.QFileDialog.getOpenFileName(filter='*.txt')
    fileName = ergebnis[0]
    parameterDict['file_Fondsliste'] = fileName
    owindow.label_NameDerDateiMitFondnamen.setText(fileName)
    LeseFondsliste()

def MacheWeiter():
    if owindow.radioButton_produktion.isChecked():
        parameterDict['environment'] = 'produktion'
        parameterDict['url_environment'] = 'https://fsl-framework.factsheetslive.com/fslmanager'
    elif owindow.radioButton_test.isChecked():
        parameterDict['environment'] = 'test'
        parameterDict['url_environment'] = 'https://fsl-framework.stg.factsheetslive.com/fslmanager'
    else:
        parameterDict['environment'] = 'fehler'
        parameterDict['url_environment'] = 'fehler'

    if Plausi() == 1:
        sys.exit()

    isin = owindow.textEdit_isin.toPlainText()
    parameterDict['isin'] = isin

    oMyKurs.ZeigeFenster(isin)


def Plausi():

    msg = QMessageBox()
    text = ''
    if parameterDict['environment'] == 'fehler':
        text = 'keine Umgebung (produktion oder Test) zugeordnet'

    if text:
        msg.setText(text)
        msg.exec_()
        return 1
    else:
        return 0

def GetProtokollDateiName(parameterDict):
    fileDir = parameterDict.get('workDirProtokoll')
    nummer = parameterDict.get('key_Einstellung')
    fileName = fileDir + 'protokoll' + '_' + str(nummer) + '.txt'
    return fileName

def NeueNummer():
    datum = datetime.date.today()
    jahr = str(datum.year).zfill(4)
    monat = str(datum.month).zfill(2)
    tag = str(datum.day).zfill(2)

    zeit = datetime.datetime.now()
    stunde = str(zeit.hour).zfill(2)
    minute = str(zeit.minute).zfill(2)
    sekunde = str(zeit.second).zfill(2)

    neuenummer = jahr + monat + tag + stunde + minute + sekunde
    return neuenummer

def LeseLetzteEinstellung(name):
    wert = oeistellung.LeseLetzteEinstellung(name)
    return wert

def BestimmeRunUmgebung():
    if owindow.radioButton_produktion.isChecked():
        parameterDict['environment'] = 'produktion'
        parameterDict['url_environment'] = 'https://fsl-framework.factsheetslive.com/fslmanager'

    elif owindow.radioButton_test.isChecked():
        parameterDict['environment'] = 'test'
        parameterDict['url_environment'] = 'https://fsl-framework.stg.factsheetslive.com/fslmanager'
    else:
        parameterDict['environment'] = 'fehler'
        parameterDict['url_environment'] = 'fehler'

    environment = parameterDict['environment']
    url = parameterDict['url_environment']
    print(f'meinMyKurs\BestimmeRunUmgebung: Die RunUmgebung wurde festgelegt: {environment}. Die URL ist : {url}')


def SchreibeFondslisteInDatei(liste):
    file = parameterDict.get('file_Fondsliste')
    f = open(file, "a")
    for element in liste:
        text = str(element) + "\n"
        f.write(text)

    f.close()


def ErstelleNeueFondsliste():
    fileDir = parameterDict.get('workDirDateien')
    nummer = NeueNummer()
    fileName = fileDir + 'fondsliste' + '_' + str(nummer) + '.txt'
    parameterDict['file_Fondsliste'] = fileName
    oKurs = myKurs.MyKurs(parameterDict)
    liste = oKurs.GetListeAllerFonds()
    text = f'Es wurde eine neue Liste erstellt diese wird in die Datei {fileName} geschrieben. Dioe Liste lautet: {liste}'
    oprot.SchreibeInProtokoll(text)

    SchreibeFondslisteInDatei(liste)
    LeseFondsliste()
    owindow.label_NameDerDateiMitFondnamen.setText(fileName)


def BestimmeAktuelleFondsliste():  # hier wird die Fondsliste bestimmt:

    # Bestimme die Run-Umgebung, bevor es losgeht:
    BestimmeRunUmgebung()

    if owindow.radioButton_alteFondsliste_ja.isChecked():
        pass
    elif owindow.radioButton_alteFondsliste_nein.isChecked():
        ErstelleNeueFondsliste()


aktuelleFondsliste = []  # in dieser Liste wird die Fondsliste für das Combobox abgelegt. Diese Liste wird gefiltert

print(f'mainKurs: übergebene Parameter {sys.argv}')
parameterDict = {}
parameterDict['workDir'] = 'D:\\Python_Projekte\\Kurse\\'
parameterDict['workDirDateien'] = 'D:\\Python_Projekte\\Kurse\\Dateien\\'
parameterDict['workDirProtokoll'] = 'D:\\Python_Projekte\\Kurse\\Protokoll\\'
parameterDict['file_WindowEinstellungen'] = parameterDict.get('workDir') + 'WindowEinstellungen.ui'
parameterDict['file_MyKursHauptfenster'] = parameterDict.get('workDir') + 'WindowKurseHauptfenster.ui'
parameterDict['environment'] = 'produktion'
parameterDict['url_environment'] = 'https://fsl-framework.factsheetslive.com/fslmanager'
parameterDict['file_Einstellung'] = parameterDict.get('workDir') + 'einstellung.csv'
parameterDict['key_Einstellung'] = NeueNummer()
parameterDict['file_Protokoll'] = GetProtokollDateiName(parameterDict)

oprot = protokoll.Protokoll(parameterDict.get('file_Protokoll'))  # das Protokoll wird angelegt
text = f'mainMaKurs: die parameter lauten: {str(parameterDict)}'
oprot.SchreibeInProtokoll(text)

oeistellung = einstellung.Einstellung(parameterDict)
oeistellung.SchreibeInEinstellung(name='parameter', text=str(parameterDict))

app = QtWidgets.QApplication(sys.argv)
file_ui = parameterDict.get('file_WindowEinstellungen')
owindow = uic.loadUi(file_ui)
owindow.pushButton_weiter.clicked.connect(MacheWeiter)
owindow.pushButton_Ende.clicked.connect(SchliesseFenster)
owindow.pushButton_DialogDateiAuswaehlen.clicked.connect(DialogDateiAuswahlen)
owindow.lineEdit_FilterFonds.textChanged.connect(FilterEintragChanged)
owindow.comboBox_Fondsliste.currentTextChanged.connect(WechselDesEintrags)
owindow.radioButton_produktion.toggled.connect(BestimmeRunUmgebung)
owindow.radioButton_alteFondsliste_ja.toggled.connect(BestimmeAktuelleFondsliste)

oMyKurs = myKurs.MyKurs(parameterDict)

if len(sys.argv) >= 2:  # d.h. abgesehen vom Workdir werden weitere Arrgumente übertragen:
    isin = sys.argv[1]  # die isin wird mit dem Aufruf von dem Modull übergeben
    parameterDict['isin'] = isin
    text = f'mainMyKurs: die ISIN ist {isin}'
    oprot.SchreibeInProtokoll(text)
    oeistellung.SchreibeInEinstellung(name='isin', text=str(isin))
    oMyKurs.SetISIN(isin)
else:
    isin_alt = LeseLetzteEinstellung('isin')  # Lese ISIN aus dem letzten Programmaufruf
    owindow.textEdit_isin.setText(isin_alt)  # Setzte die alte ISIN in das Dialog rein

    owindow.show()

app.exec_()

