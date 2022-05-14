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
        x,y=[],[]
        for i in range (len(datos[:,0])):
            x.append(datos[:,0][i])
        for i in range (len(datos[:,1])):
            y.append(datos[:,1][i])
        pen = pg.mkPen(color=(255, 255, 255))
        self.graph_data.plot(x, y,pen=pen,symbol='x',symbolSize=10)

        #grafico 2 costo
        for i in range(itr):
            costo,theta=self.reg._calculo_gradiente()
            self.reg.theta=theta

            itr_arr.append(i)
            costo_arr.append(costo)
            # theta1_arr.append(theta[0])
            # theta2_arr.append(theta[1])

            self.cost_line.setData(itr_arr, costo_arr)
            self.itr_progress.setValue(int((i+1)*100/itr))

        #resultados
        self.theta1_input.setValue(theta[0])
        self.theta2_input.setValue(theta[1])
        
        #grafico 3 3D
        theta0arr=np.arange(self.reg.minTheta[0]*2,self.reg.maxTheta[0],0.4)
        theta1arr=np.arange(self.reg.minTheta[1]*2,self.reg.maxTheta[1],0.125)
        # print(theta1arr.size,theta0arr.size)
        theta0arr, theta1arr = np.meshgrid(theta0arr, theta1arr)
        J = np.zeros((theta0arr.size, theta1arr.size))
        print(J)
        for index, v in np.ndenumerate(J):
            print(index)
            J[index] = self.reg.costo([theta0arr[index],theta1arr[index]])    
        # xs = np.arange(-10, 10, 0.4)
        # ys = np.arange(-2, 5, 0.14)
        # xx, yy = np.meshgrid(xs, ys)
        # J = np.zeros((xs.size, ys.size))
        # for index, v in np.ndenumerate(J):
        #     J[index] = self.reg.costo([xx[index],yy[index]])    
        # z=pg.gaussianFilter(np.random.normal(size=(25,25)), (1,1))
        p1 = gl.GLSurfacePlotItem(z=J, shader='shaded', color=(0.5, 0.5, 1, 1))
        
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