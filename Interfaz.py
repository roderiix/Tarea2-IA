import numpy as np
import Graficos
x=[]
y=[]
thetha = np.zeros((1, 2))

archivo=open("data1.txt","r")
linea=archivo.readline().strip()
while linea != "":
    partes=linea.split(",")
    x.append(float(partes[0]))
    y.append(float(partes[1]))             
    linea=archivo.readline().strip()
archivo.close()

Graficos.Graficos().grafico1(x,y)