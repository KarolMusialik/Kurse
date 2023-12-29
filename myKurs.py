import WindowMyKursHauptfenster

class MyKurs:

    def __init__(self, parameterDict):
        self.parameterDict = parameterDict
        self.owindow = WindowMyKursHauptfenster.WindowsMyKursHauptfenster(self.parameterDict)


    def ZeigeFenster(self, isin, initDict):
        print('MyKurs/ZeigeFenster: hier soll der Dialog aufgerufen werden')
        self.owindow.InitFenster(initDict)
        self.RufeAlleFunktionenAuf(isin)
        self.SchreibeDokumenteInsDialog()
        self.owindow.zeigeFenster()


    def GetListeAllerFonds(self):
        liste = self.owindow.GetListeAllerFonds()
        return liste

    def SchreibeDokumenteInsDialog(self):
        self.owindow.SchreibeDokumenteInsDialog()


    def SetISIN(self, isin):
        self.owindow.isin = isin

    def LeseInfosZuIsin(self, isinInfosDict):

        self.owindow.LeseInfosZuIsin(isinInfosDict)


    def RufeAlleFunktionenAuf(self, isin):
        self.owindow.isin = isin  # ISIN wird festgelegt
        self.owindow.InvestorTypeList()  # InvestortypeCode und InvestorTypeName werden festgelegt
        self.owindow.InvestorCountryList()  # Sprache wird eingestellt
        # self.owindow.PageList()
        # self.owindow.EvaluatedPageList()
        # self.owindow.EvaluatedParameterCombinations()
        self.owindow.ProductList()
        self.owindow.HistoricPriceData()
        self.owindow.ProductData(isin)
        self.owindow.Documents()
        self.owindow.AllocationDate()

