from pathlib import Path
import pandas as pd

class Einstellung:

    def __init__(self, fileDict):
        self.file = fileDict.get('file_Einstellung')

    def SetKey(self, key):
        self.key = key

    def SchreibeInEinstellung(self, name, text):

        text = self.key + ";" + str(name) + ";" + str(text) + "\n"
        f = open(self.file, "a")
        f.write(text)
        f.close()

    def LeseInhaltEinstellung(self, key, name):
        wert = ''
        df = pd.read_csv(self.file, sep=";")
        df1 = df[df.key == key]

        if df1.empty:
            wert = 0
            text = 'Optionen/LeseInhaltOptionen: Kein Eintrag gefunden. Es wurde null verwendet: key=' + str(print(key))
            print(text)
        else:
            index = df1.index[0]
            wert = df1.at[index, 'wert']

        return wert

    def LeseLetzteEinstellung(self, name):
        wert = ''
        df = pd.read_csv(self.file, sep=";")
        df1 = df[df.name == name]

        if df1.empty:
            wert = ''
            text = f'Einstellung/LeseLetzteEinstellung: Kein Eintrag zu {str(name)} gefunden. Es wird null verwendet'
            print(text)
            return wert

        if len(df1 == 1):  # alles okay. Es darf nur einen geben:
            index = df1.index[0]
            wert = df1.at[index, 'text']
            return wert
        else:  # ojej! es wurden mehrere Einträge gefunden. Fehler!
            wert = ''
            text = f'Einstellung/LeseLetzteEinstellung: Es wurden mehrere Einträge zu {str(name)} gefunden. Es wird null verwendet'
            print(text)
            return wert

