from asyncio import sleep
import sys
from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
from Reader import Reader
from Regresion import Regresion
import time
qtCreatorFile = "form.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        reader = Reader('data1.txt')
        self.datos = reader.txt_to_array()
        self.graph_cost.setTitle("Your Title Here", color="black", size="15pt")
        self.graph_cost.setBackground('w')
        # print(datos[:,0])
        # hour = datos[:,0]
        # temperature = datos[:,1]

        # self.graph_data.setTitle("Your Title Here", color="black", size="15pt")

        # pen = pg.mkPen(color=(255, 255, 255))

        # self.graph_data.setBackground('w')
        self.graph_cost.plot()
        # self.graph_data.plot(hour, temperature,pen=pen,symbol='+',symbolSize=10)    
        self.btn_start.clicked.connect(lambda:self.grafico2())

    def grafico2(self):
        reg=Regresion(self.datos)
        x=[]
        y=[]
        for i in range(self.itr_input.value()):
            costo,theta=reg._calculo_gradiente()
            reg.theta=theta
            x.append(i)
            y.append(costo)
            if(i%100==0): 
                self.graph_cost.plot(x,y) 
app =  QtWidgets.QApplication(sys.argv)
window = MyApp()
window.show()
sys.exit(app.exec_())