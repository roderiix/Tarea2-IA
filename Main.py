from copy import copy
import sys
from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import pyqtgraph.opengl as gl
from Reader import Reader
from Regresion import Regresion
from misc import *
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
        self.running = False
        self.stop = False

        styles = {'color':'r', 'font-size':'20px'}
        self.graph_cost.setTitle("Costo por Iteracion", color="black", size="15pt")
        self.graph_cost.setBackground('w')
        self.graph_cost.setLabel('left', "<span style=\"color:gray;font-size:15px\">Costo</span>")
        self.graph_cost.setLabel('bottom', "<span style=\"color:gray;font-size:15px\">Iteracion</span>")

        self.graph_data.setTitle("Habitantes/Precio", color="black", size="15pt")
        self.graph_data.setBackground('w')
        self.graph_data.setLabel('left', "<span style=\"color:gray;font-size:15px\">Precio</span>")
        self.graph_data.setLabel('bottom', "<span style=\"color:gray;font-size:15px\">Habitantes</span>")

        self.graph_25d.setBackground('w')
        self.graph_25d.setLabel('left', "<span style=\"color:gray;font-size:15px\">thetha 0</span>")
        self.graph_25d.setLabel('bottom', "<span style=\"color:gray;font-size:15px\">thetha 1</span>")

        self.graph_3d.opts['distance'] = 75
        self.graph_3d.show()
        self.direccion=self.file_path.text()
        large=40
        gx = gl.GLGridItem()
        gx.setSize(large,large,large)
        gx.rotate(90, 0, 1, 0)
        gx.translate(-large/2, 0, 0)
        self.graph_3d.addItem(gx)
        gy = gl.GLGridItem()
        gy.setSize(large,large,large)
        gy.rotate(90, 1, 0, 0)
        gy.translate(0, -large/2, 0)
        self.graph_3d.addItem(gy)
        gz = gl.GLGridItem()
        gz.setSize(large,large,large)
        gz.translate(0, 0, -large/2)
        self.graph_3d.addItem(gz)
        
        self.cost_line = self.graph_cost.plot()
        self.graph_data.plot()
        self.btn_start.clicked.connect(lambda:self.verificarArchivo())
        self.search_btn.clicked.connect(lambda:self.probar_valor())
        self.btn_buscar.clicked.connect(lambda:self.buscarArchivo())

    def Msj_Error(self):
        EntryMsg = QMessageBox()
        EntryMsg.setIcon(QMessageBox.Warning)
        EntryMsg.setWindowTitle('Error!')
        EntryMsg.setText('No hay archivo seleccionado')
        EntryMsg.setStandardButtons(QMessageBox.Ok)
        EntryMsg.setDefaultButton(QMessageBox.Ok)
        EntryMsg.exec_()

    def buscarArchivo(self):
        fname = QFileDialog.getOpenFileName(self, 'Buscar archivo', '', 'Data File (*.txt)'),
        if fname:
            self.file_path.setText(str(fname[0][0]))
            self.direccion=self.file_path.text()

    def verificarArchivo(self):
        if self.direccion: self.grafico()
        else: self.Msj_Error()

    def grafico(self):

        # if self.running and not self.stop and self.btn_start.text() == 'Abortar':
        #     self.stop = True
        # else:
        #     self.running = True
        #     self.btn_start.setText('Abortar')
        self.graph_data.clear()
        # self.graph_cost.clear()
        # self.graph_3d.clear()

        itr = self.itr_input.value()
        alpha = self.alpha_input.value()

        reader = Reader(self.direccion)
        datos = reader.txt_to_array()

        self.reg=Regresion(data=datos, alpha=alpha)
        # if self.running and self.stop:
        #     self.btn_start.setText('Iniciar')
        #     self.running = False
        #     self.stop = False
        #     self.itr_progress.setValue(0)
        #     return
    
        # 1 - graph data
        x1,y1=[],[]
        for i in range (len(datos[:,0])):
            x1.append(datos[:,0][i])
            y1.append(datos[:,1][i])
        pen = pg.mkPen(color=(255, 255, 255))
        self.graph_data.plot(x1, y1,pen=pen,symbol='x',symbolSize=10)    

        #2 - graph 3d surface

        # xs=np.linspace(self.reg.minTheta[0],self.reg.maxTheta[0],50)
        # ys=np.linspace(self.reg.minTheta[1],self.reg.maxTheta[1],50)
        xs=np.linspace(-10,10,50)
        ys=np.linspace(-10,10,50)
        theta0arr, theta1arr = np.meshgrid(xs, ys)
        J = np.zeros((xs.size, ys.size))

        for index, v in np.ndenumerate(J):
            J[index] = self.reg.costo([theta0arr[index],theta1arr[index]])

        p1 = gl.GLSurfacePlotItem(x=xs,y=ys,z=J/100, shader='normalColor')
        p1.translate(0, 0, -15)
        self.graph_3d.addItem(p1)

        #4 - graph contour

        # theta0arr=np.cos(theta0arr)
        # theta1arr=np.sin(theta1arr)
        # contour_theta = np.append(np.reshape(theta0arr, (theta0arr.size, 1)),np.reshape(theta1arr, (theta1arr.size, 1)) , axis=1)

        contour_theta=np.sin(theta0arr) + np.cos(theta1arr)
        pen = pg.mkPen(color=(0, 0, 0))
        contour = pg.IsocurveItem(contour_theta,pen=pen)
        self.graph_25d.addItem(contour)

        # "real time" graph update
        self.execute_regression(itr, alpha, datos)

        # output theta
        self.theta1_input.setValue(self.reg.theta[0])
        self.theta2_input.setValue(self.reg.theta[1])

    def probar_valor(self):
        value = self.test_input.value()
        try:
            self.result_output.setValue(self.reg.hipotesis(value))
        except:
            pass

    def execute_regression(self, itr, alpha, datos):

        cost_arr = []
        itr_arr = []

        graph_data_item = None
        for i in range(itr):
            if self.running and self.stop: return
            costo,theta=self.reg._calculo_gradiente(set_value=True)
            cost_arr.append(costo)
            itr_arr.append(i)

            # update cost graph
            self.cost_line.setData(itr_arr, cost_arr)

            #update progress bar
            self.itr_progress.setValue(int((i+1)*100/itr))

            #update 3d graph
                
            # if(i%100==0):
            #     fig=gl.GLScatterPlotItem(pos=np.append(theta,costo))
            #     # fig.translate(0, 0, -10)
            #     self.graph_3d.addItem(fig)

            #update data graph
                # actualizar la posicion de la recta hipotesis
            # valorX = np.arange(4, 27) 
            # valorY =[]
            # for i in valorX:
            #     valorY.append(self.reg.hipotesis(i))
            # pen = pg.mkPen(color=(0, 0, 0))
            # self.graph_data.plot(valorX, valorY,pen=pen)

            # infinite line
            if graph_data_item:
                self.graph_data.removeItem(graph_data_item)
            graph_data_item = pg.InfiniteLine(
                pos=[0, self.reg.hipotesis(0)],
                movable=False,
                angle=degree([itr,self.reg.hipotesis(itr)],[1,0]),
                pen='g'
            )
            self.graph_data.addItem(graph_data_item)

            QtWidgets.QApplication.processEvents()

app =  QtWidgets.QApplication(sys.argv)
window = MyApp()
window.show()
sys.exit(app.exec_())