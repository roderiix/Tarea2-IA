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
hipotesis = reg.hipotesis(x=[0,0,0])
print(f'hipotesis de x={[0,0,0]}: {hipotesis}')

# costo
costo =reg.cost(theta=[0,0,0])
print(f'costo de x={[0,0,0]}: {costo}')

# optimize
costo, theta = reg.optimize(theta=[0,0,0])
print(f'Theta: {theta}')
print(f'costo: {costo}')

# prediction
prediction = reg.predict(x=[0,0,0], theta=theta)
# print(f'probabilidad: {prob}')
print(f'prediccion de x={[0,0,0]}: {prediction}')

# perfomance
recall, precision, fmeasure = reg.perfomance()
print(f'recall: {recall}')
print(f'precision: {precision}')
print(f'f-measure: {fmeasure}')
