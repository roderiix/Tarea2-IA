from tkinter import Y
import numpy as np

class IA:
    x=[]
    y=[]
    X1=[]
    Y1=[]
    thetha = np.zeros((1, 2))
    thethaTrans=np.transpose(thetha)
    costo=0

    def __init__(self):
        archivo=open("data1.txt","r")
        linea = archivo.readline().strip()
        while linea != "":
            partes=linea.split(",")
            self.x.append(float(partes[0]))
            self.y.append(float(partes[1]))             
            linea=archivo.readline().strip()
        archivo.close()
        self.X1 = np.array(self.x)
        self.Y1 = np.array(self.y)
        m = len(self.X1)
        aux = np.ones((m,1))
        self.X1 = np.reshape(self.X1,(m,1))
        self.X1 = np.append(aux,self.X1,axis=1)
        self.costo = IA.funcionCosto(self.X1,self.Y1,self.thethaTrans)


    def funcionCosto(X, Y, theta):
        m = len(Y)
        aux = X.dot(theta)
        aux = aux.transpose() - Y
        J = np.sum(aux**2)/(2*m)    
        return J

    def GradienteDescendiente(self,alpha,num_iter):
        X = self.X1
        Y = self.Y1
        theta = self.thethaTrans
        J = []
        m = len(X)
        J = np.zeros(shape=(num_iter, 1))
        
        for i in range (num_iter):
            aux = X.dot(theta).flatten()
            x1 = (aux - Y) * X[:, 0]
            x2 = (aux - Y) * X[:, 1]
            theta[0][0] = theta[0][0] - alpha * (1 / m) * x1.sum()
            theta[1][0] = theta[1][0] - alpha * (1 / m) * x2.sum()
            J[i, 0] = IA.funcionCosto(X, Y, theta)
        return J,theta