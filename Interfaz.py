import numpy as np
import Graficos
import IA

Graficos.Graficos().grafico1(IA.IA().x,IA.IA().y)

alpha=0.01
num=1500
J,thetaGD = IA.IA().GradienteDescendiente(alpha,num)
print(thetaGD)
print('------------------------')
print(J)
theta1 = list(thetaGD)

print(theta1)