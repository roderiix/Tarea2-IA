from asyncio import sleep
import sys
from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox, QFileDialog
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

        self.graph_3d.opts['distance'] = 75
        self.graph_3d.show()
        self.direccion=''
        tamania=40
        gx = gl.GLGridItem()
        gx.setSize(tamania,tamania,tamania)
        gx.rotate(90, 0, 1, 0)
        gx.translate(-20, 0, 0)
        self.graph_3d.addItem(gx)
        gy = gl.GLGridItem()
        gy.setSize(tamania,tamania,tamania)
        gy.rotate(90, 1, 0, 0)
        gy.translate(0, -20, 0)
        self.graph_3d.addItem(gy)
        gz = gl.GLGridItem()
        gz.setSize(tamania,tamania,tamania)
        gz.translate(0, 0, -20)
        self.graph_3d.addItem(gz)
        
        self.cost_line = self.graph_cost.plot()
        self.graph_data.plot()
        self.btn_start.clicked.connect(lambda:self.verificarArchivo())
        self.search_btn.clicked.connect(lambda:self.probar_valor())
        self.btn_buscar.clicked.connect(lambda:self.buscarArchivo())
        self.btn_leerArchivo.clicked.connect(lambda:self.leerArchivo())


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
    
    def leerArchivo(self):
        self.direccion=self.file_path.text()

    def verificarArchivo(self):
        if self.direccion: self.grafico()
        else: self.Msj_Error()

    def grafico(self):

        itr = self.itr_input.value()
        alpha = self.alpha_input.value()

        reader = Reader(self.direccion)
        datos = reader.txt_to_array()
        self.reg=Regresion(data=datos, alpha=alpha)

        itr_arr = []
        costo_arr = []
    


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

            self.cost_line.setData(itr_arr, costo_arr)
            self.itr_progress.setValue(int((i+1)*100/itr))

        #resultados
        self.theta1_input.setValue(theta[0])
        self.theta2_input.setValue(theta[1])

        valorX = np.arange(4, 27) 
        valorY =[]
        for i in valorX:
            valorY.append(self.reg.hipotesis(i))
        pen = pg.mkPen(color=(0, 0, 0))
        self.graph_data.plot(valorX, valorY,pen=pen)
        #grafico 3 3D
        xs=np.linspace(self.reg.minTheta[0],self.reg.maxTheta[0],50)
        ys=np.linspace(self.reg.minTheta[1],self.reg.maxTheta[1],50)
        # xs = np.arange(-10, 10, 0.4)
        # ys = np.arange(-2, 5, 0.14)
        theta0arr, theta1arr = np.meshgrid(xs, ys)
        J = np.zeros((xs.size, ys.size))
        for index, v in np.ndenumerate(J):
            J[index] = self.reg.costo([theta0arr[index],theta1arr[index]])

        p1 = gl.GLSurfacePlotItem(x=xs*10,y=ys*20,z=J/2, shader='normalColor')
        p1.translate(20, -10, -10)
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