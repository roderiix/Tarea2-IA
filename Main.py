from asyncio import sleep
import sys
from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import pyqtgraph.opengl as gl
from Reader import Reader
from Regresion import Regresion
import time
import numpy as np
qtCreatorFile = "form.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.alpha_input.setValue(0.01)
        self.alpha_input.setRange(-1., 1.)
        self.theta1_input.setRange(-9999, 9999)
        self.theta2_input.setRange(-9999, 9999)
        self.result_output.setRange(-9999, 9999)

        self.graph_cost.setTitle("Costo por Iteracion", color="black", size="15pt")
        self.graph_cost.setBackground('w')

        self.graph_data.setTitle("Habitantes/Precio", color="black", size="15pt")
        self.graph_data.setBackground('w')

        self.graph_3d.opts['distance'] = 40
        self.graph_3d.show()

        gx = gl.GLGridItem()
        gx.rotate(90, 0, 1, 0)
        gx.translate(-10, 0, 0)
        self.graph_3d.addItem(gx)
        gy = gl.GLGridItem()
        gy.rotate(90, 1, 0, 0)
        gy.translate(0, -10, 0)
        self.graph_3d.addItem(gy)
        gz = gl.GLGridItem()
        gz.translate(0, 0, -10)
        self.graph_3d.addItem(gz)
        
        self.cost_line = self.graph_cost.plot()
        self.graph_data.plot()
        self.btn_start.clicked.connect(lambda:self.grafico())
        self.search_btn.clicked.connect(lambda:self.probar_valor())

    def grafico(self):

        itr = self.itr_input.value()
        alpha = self.alpha_input.value()

        reader = Reader('data1.txt')
        datos = reader.txt_to_array()
        self.reg=Regresion(data=datos, alpha=alpha)

        itr_arr = []
        costo_arr = []
        theta1_arr = []
        theta2_arr = []


        # grafico 1 datos
        pen = pg.mkPen(color=(255, 255, 255))
        self.graph_data.plot(datos[:,0], datos[:,1],pen=pen,symbol='+',symbolSize=10)

        #grafico 2 costo
        for i in range(itr):
            costo,theta=self.reg._calculo_gradiente()
            self.reg.theta=theta

            itr_arr.append(i)
            costo_arr.append(costo)
            theta1_arr.append(theta[0])
            theta2_arr.append(theta[1])

            self.cost_line.setData(itr_arr, costo_arr)
            self.itr_progress.setValue(int(i*100/itr)+1)

        #resultados
        self.theta1_input.setValue(theta[0])
        self.theta2_input.setValue(theta[1])
        
        #grafico 3 3D
        p1 = gl.GLSurfacePlotItem(x=np.array(theta1_arr),y=np.array(theta2_arr),z=np.array(costo_arr), shader='shaded', color=(0.5, 0.5, 1, 1))
        self.graph_3d.addItem(p1)
        

    def probar_valor(self):
        value = self.test_input.value()
        try:
            self.result_output.setValue(self.reg.hipotesis(value))
        except:
            pass

        

app =  QtWidgets.QApplication(sys.argv)
window = MyApp()
window.show()
sys.exit(app.exec_())