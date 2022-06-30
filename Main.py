import sys
import os
from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
from matplotlib import pyplot as plt
from Reader import Reader
from Regresion import Regresion
from misc import *
import numpy as np
qtCreatorFile = "form.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.alpha_input.setValue(0.01)

        self.graph_cost.setTitle("Costo por Iteracion", color="black", size="15pt")
        self.graph_cost.setBackground('w')
        self.graph_cost.setLabel('left', "<span style=\"color:gray;font-size:15px\">Costo</span>")
        self.graph_cost.setLabel('bottom', "<span style=\"color:gray;font-size:15px\">Iteracion</span>")

        self.graph_data.setTitle("Habitantes/Precio", color="black", size="15pt")
        self.graph_data.setBackground('w')
        self.graph_data.setLabel('left', "<span style=\"color:gray;font-size:15px\">Precio</span>")
        self.graph_data.setLabel('bottom', "<span style=\"color:gray;font-size:15px\">Habitantes</span>")

        self.direccion=self.file_path.text()
        
        self.cost_line = self.graph_cost.plot()
        self.graph_data.plot()
        self.btn_start.clicked.connect(lambda:self.verificarArchivo())
        self.search_btn.clicked.connect(lambda:self.probar_valor())
        self.btn_buscar.clicked.connect(lambda:self.buscarArchivo())
        self.btnGraphContorno.clicked.connect(lambda:self.GraphContorno())
        self.btnGraph3D.clicked.connect(lambda:self.grafico3D())
        self.btnNormal.clicked.connect(lambda:self.graphNormal())
        self.btnGraph3D.setEnabled(False)
        self.btnGraphContorno.setEnabled(False)
        self.btnNormal.setEnabled(False)

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
        if os.path.exists(self.direccion): self.grafico()
        else: self.Msj_Error()

    def grafico(self):
        self.btn_start.setEnabled(False)
        self.graph_data.clear()

        itr = self.itr_input.value()
        alpha = self.alpha_input.value()

        reader = Reader(self.direccion)
        datos = reader.txt_to_array()

        self.reg=Regresion(data=datos, theta= np.array([self.theta1_input.value(), self.theta2_input.value()]), alpha=alpha)
    
        # 1 - graph data
        x1,y1=[],[]
        for i in range (len(datos[:,0])):
            x1.append(datos[:,0][i])
            y1.append(datos[:,1][i])
        pen = pg.mkPen(color=(255, 255, 255))
        self.graph_data.plot(x1, y1,pen=pen,symbol='x',symbolSize=10)    

        # "real time" graph update
        self.execute_regression(itr)

        # out result
        self.theta0f.setValue(self.reg.theta[0])
        self.theta1f.setValue(self.reg.theta[1])
        self.theta0n.setValue(self.reg.normal()[0])
        self.theta1n.setValue(self.reg.normal()[1])
        self.resultado35.setValue(self.reg.hipotesis(3.5))
        self.resultado75.setValue(self.reg.hipotesis(7))
        self.btnGraph3D.setEnabled(True)
        self.btnGraphContorno.setEnabled(True)
        self.btnNormal.setEnabled(True)
        self.btn_start.setEnabled(True)

    def probar_valor(self):
        value = self.test_input.value()
        try: self.result_output.setValue(self.reg.hipotesis(value))
        except: pass

    def execute_regression(self, itr):

        itr_arr = []

        graph_data_item = None
        for i in range(itr):
            costo,_= self.reg._calculo_gradiente(set_value=True)
            itr_arr.append(i)

            # udpdate data graph line
            if graph_data_item:
                self.graph_data.removeItem(graph_data_item)
            graph_data_item = pg.InfiniteLine(
                pos=[0, self.reg.hipotesis(0)],
                movable=False,
                angle=degree([itr,self.reg.hipotesis(itr)],[1,0]),
                pen='g'
            )
            self.graph_data.addItem(graph_data_item)

            # update cost graph
            self.cost_line.setData(itr_arr, self.reg.historial['costo'])

            #update progress bar
            self.itr_progress.setValue(int((i+1)*100/itr))
            self.costoF.setValue(costo)
            QtWidgets.QApplication.processEvents()
    
    def GraphContorno(self):
        fig = plt.figure()
        ax2 = fig.add_subplot()
        ax2.contour(self.reg.grid['x'], self.reg.grid['y'], self.reg.grid['costo'], np.logspace(-2, 3, 20), cmap='jet')
        ax2.plot(self.reg.theta[0], self.reg.theta[1], 'rx')
        ax2.set_title('Contorno de la funcion de Costo')

        for i in range(0,self.itr_input.value(),int(self.itr_input.value()/10)):
            ax2.plot(self.reg.historial['theta'][i][0], self.reg.historial['theta'][i][1], 'bo')
        plt.show()

    def grafico3D(self):
        fig = plt.figure()
        g3d = fig.add_subplot( projection='3d')
        g3d.plot_surface(self.reg.grid['x'], self.reg.grid['y'], self.reg.grid['costo'], alpha=0.5, cmap='jet')
        g3d.set_zlabel('Costo', fontsize=12)
        g3d.set_title('Superficie de la funcion de costo')
        for i in range(0,self.itr_input.value(),int(self.itr_input.value()/10)):
            g3d.plot(self.reg.historial['theta'][i][0], self.reg.historial['theta'][i][1],self.reg.historial['costo'][i], 'bo')
        plt.show()
    
    def graphNormal(self):
        plt.figure(figsize=(12, 8))
        plt.title("Ecuacion Normal")
        plt.plot(self.reg.normal())
        plt.grid()
        plt.show()


app =  QtWidgets.QApplication(sys.argv)
window = MyApp()
window.show()
sys.exit(app.exec_())