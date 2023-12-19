import sys
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from pathlib import Path
class WindowDiagrammm:

    def __init__(self, initDict):
        self.file_ui = initDict.get('workDir')+'Diagramm.ui'
        datei = Path(self.file_ui)
        self.window = uic.loadUi(datei)

        self.file = initDict.get('file')
        self.window.setWindowTitle(self.file)

        pixmap = QPixmap(self.file)
        pixmap2 = pixmap.scaled(self.window.label_Diagramm.size())
        self.window.label_Diagramm.setPixmap(pixmap2)

        self.window.exec_()