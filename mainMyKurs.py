import sys
import MyKurs
from PyQt5 import QtWidgets
import PyQt5.uic as uic
from PyQt5.QtWidgets import QMessageBox
import pandas as pd
from pathlib import Path

if __name__ == '__main__':

    isin = "LU1675428244"  # Standartwert
    aktuelleFondsliste = []  # in dieser Liste wird die Fondsliste für das Combobox abgelegt. Diese Liste wird gefiltert

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


        df = pd.read_csv(datei_path, sep=';')
        print(df)

        if df.empty:
            print(f'LeseFondsliste: Datei {datei} ist leer. Fehler! Abbruch')
            sys.exit()

        anzahl = df['isin'].count()

        aktuelleFondsliste.clear()
        izeile = -1
        for index, row in df.iterrows():
            izeile += 1
            isin = row[0]
            name = row[1]
            eintrag = isin + '_' + name
            aktuelleFondsliste.append(eintrag)

        SchreibeAktuelleListeInComboBox()

        owindow.comboBox_Fondsliste.currentTextChanged.connect(WechselDesEintrags)
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


    print(f'mainKurs: übergebene Parameter {sys.argv}')
    parameterDict = {}
    parameterDict['workDir'] = 'D:\\Python_Projekte\\Kurse\\'
    parameterDict['file_WindowEinstellungen'] = parameterDict.get('workDir') + 'WindowEinstellungen.ui'
    parameterDict['file_MyKursHauptfenster'] = parameterDict.get('workDir') + 'WindowKurseHauptfenster.ui'
    parameterDict['file_Fondsliste'] = parameterDict.get('workDir') + 'fondsliste.txt'
    parameterDict['environment'] = 'produktion'
    parameterDict['url_environment'] = 'https://fsl-framework.factsheetslive.com/fslmanager'

    app = QtWidgets.QApplication(sys.argv)
    file_ui = parameterDict.get('file_WindowEinstellungen')
    owindow = uic.loadUi(file_ui)

    oMyKurs = MyKurs.MyKurs(parameterDict)

    if len(sys.argv) >= 2:  # d.h. abgesehen vom Workdir werden weitere Arrgumente übertragen:
        isin = sys.argv[1]  # die isin wird mit dem Aufruf von dem Modull übergeben
        parameterDict['isin'] = isin
        oMyKurs.SetISIN(isin)
    else:

        aktuelleFondsliste = oMyKurs.GetListeAllerFonds()
        SchreibeAktuelleListeInComboBox()

        owindow.pushButton_weiter.clicked.connect(MacheWeiter)
        owindow.pushButton_Ende.clicked.connect(SchliesseFenster)
        owindow.lineEdit_FilterFonds.textChanged.connect(FilterEintragChanged)
        owindow.comboBox_Fondsliste.currentTextChanged.connect(WechselDesEintrags)

        owindow.show()

    app.exec_()


