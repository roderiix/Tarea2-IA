import sys
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMessageBox
qtCreatorFile = "form.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

app =  QtWidgets.QApplication(sys.argv)
window = MyApp()
window.show()
sys.exit(app.exec_())