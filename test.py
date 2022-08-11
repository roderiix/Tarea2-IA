import numpy as np
from Reader import Reader
from Regresion import Regresion

reader = Reader('ex2data1.txt')
data = reader.get_data()
# data = [[x0,x1,x2], y]

# group0, group1 = reader.get_groups()

# separar data en 2 grupos, al 80% y 20%, aleatorio
training_data = data[np.random.choice(data.shape[0], 80, replace=False)]
# test_data = np.setdiff1d(data, training_data, False)

# separar data en 2 grupos, al 80% y 20%, no-aleatorio
training_data = data[0:80,:]
test_data = data[80:,:]
reg = Regresion(training_data=training_data, test_data=test_data)

# hipotesis
x = [0,0,0]
hipotesis = reg.hipotesis(x=x)
print(f'Testeo Hipotesis')
print(f'\tx: {x}')
print(f'\tresultado: {round(hipotesis, 3)}')

# costo
costo =reg.cost(theta=x)
print(f'Testeo Costo')
print(f'\tx: {x}')
print(f'\ttheta utilizado: {reg.theta}')
print(f'\tresultado: {round(costo, 3)}')

# optimize
theta_inicial = [0,0,0]
costo, theta = reg.optimize(theta=theta_inicial)
print(f'Optimizacion')
print(f'\tTheta inicial: {theta_inicial}')
print(f'\tTheta minimo: {theta}')
print(f'\tCosto: {round(costo, 3)}')

# prediction
# x = [
#     1.,
#     float(input('Ingrese examen N1: ')),
#     float(input('Ingrese examen N2: '))
# ]
x = [0,0,0]
probabilidad, prediction = reg.predict(x=x, theta=theta)
print(f'Prediccion')
print(f'\tx: {x}')
print(f'\ttheta utilizado: {reg.theta}')
print(f'\tprobabilidad: {probabilidad}')
print(f'\tresultado: {prediction}')

# perfomance
recall, precision, fmeasure = reg.perfomance()
print('Rendimiento')
print(f'\trecall: {recall}')
print(f'\tprecision: {precision}')
print(f'\tf-measure: {fmeasure}')
