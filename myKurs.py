import WindowMyKursHauptfenster

class MyKurs:

    def __init__(self, parameterDict):
        self.parameterDict = parameterDict
        self.owindow = WindowMyKursHauptfenster.WindowsMyKursHauptfenster(self.parameterDict)


    def ZeigeFenster(self, isin, initDict):
        print('MyKurs/ZeigeFenster: hier soll der Dialog aufgerufen werden')
        self.owindow.InitFenster(initDict)
        self.RufeAlleFunktionenAuf(isin)
        self.owindow.zeigeFenster()


    def GetListeAllerFonds(self):
        liste = self.owindow.GetListeAllerFonds()
        return liste


    def SetISIN(self, isin):
        self.owindow.isin = isin


    def RufeAlleFunktionenAuf(self, isin):
        self.owindow.isin = isin
        self.owindow.InvestorTypeList()
        self.owindow.InvestorCountryList()
        self.owindow.PageList()
        self.owindow.EvaluatedPageList()
        self.owindow.EvaluatedParameterCombinations()
        self.owindow.ProductList()
        self.owindow.HistoricPriceData()
        self.owindow.ProductData(isin)
        self.owindow.Documents()
        self.owindow.AllocationDate()

