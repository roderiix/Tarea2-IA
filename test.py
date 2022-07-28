import numpy as np
from scipy.optimize import minimize, fmin
from scipy.special import expit
from Reader import Reader
from Regresion import Regresion

reader = Reader('ex2data1.txt')
x,y = reader.get_data()
# [[x0,x1,x2], y]

# group0, group1 = reader.get_groups()

reg = Regresion(data=[x,y])

# # hipotesis
# print(reg.predict(x=[0,0,0]))

# # costo
# print(reg.cost(theta=[0,0,0]))

# # optimzie
# print(reg.theta)
costo, theta = reg.optimize(theta=[0,0,0])
# print(reg.theta)
# print(f'costo: {costo}')

print(reg.predict(reg.x, theta))
