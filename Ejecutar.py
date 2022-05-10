import sys
from PyQt5 import uic, QtWidgets
import Graficos
import IA
from PyQt5.QtWidgets import QMessageBox
qtCreatorFile = "untitled.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.Btn_Grafico1.clicked.connect(self.grafico1)

    def grafico1(self):
        Graficos.Graficos().grafico1(IA.IA().x,IA.IA().y)

app =  QtWidgets.QApplication(sys.argv)
window = MyApp()
window.show()
sys.exit(app.exec_())