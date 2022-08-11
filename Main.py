from Reader import Reader
from Regresion import Regresion
import matplotlib.pyplot as pl
import numpy as np
from tabulate import tabulate

# empezar con objeto de clase regresion con set training al 100%, sin set de testeo
reader = Reader('ex2data1.txt')
data = reader.get_data()
#<<<<<<< HEAD
#=======
regresion = Regresion(training_data = data)

print(f'\n----------------------------------------------\n')

#>>>>>>> c7dbcd1b43cf04a0ca3532dfe5dd972a65c5d354
# 1.- grafico dispersion
group0, group1 = reader.get_groups()
def scatter_plot(func = lambda: None):
    pl.scatter(x=group0[:,1], y=group0[:,2], color='red', marker = 'o', label='No admitido')
    pl.scatter(x=group1[:,1], y=group1[:,2], color='blue', marker = '*', label='Admitido')
    pl.xlabel('Examen 1')
    pl.ylabel('Examen 2')
    pl.title('Clasificador Binario')
    func()
    pl.legend()
    pl.show()

scatter_plot()

#hola
reg = Regresion(training_data=data)

# 2.- funcion sigmoidal
#<<<<<<< HEAD
x = [0,0,0]
prediccion = regresion.hipotesis(x=x)
print(f'Testeo Hipotesis')
print(f'\tx: {x}')
print(f'\tresultado: {round(prediccion, 3)}')

# 3.- funcion costo
costo = regresion.cost()
print(f'Testeo Costo')
print(f'\tx: {x}')
print(f'\ttheta utilizado: {regresion.theta}')
print(f'\tresultado: {round(costo, 3)}')

# 4.- optimizacion
theta_inicial = [0,0,0]
costo, theta = regresion.optimize(theta=theta_inicial)
print(f'Testeo Optimizacion')
print(f'\tTheta inicial: {theta_inicial}')
print(f'\tTheta optimo: {theta}')
print(f'\tCosto: {round(costo, 3)}')
# 4.1- grafico
def graph_boundary():
    x_boundary = np.array([np.min(data[:,1]), np.max(data[:,1])])
    y_boundary = -(theta[0] + theta[1]*x_boundary)/theta[2]
    pl.axline(x_boundary, y_boundary, color='mediumpurple' ,label='Limite de decision')
scatter_plot(graph_boundary)

# 5.- prediccion
x = [1, 45., 85.]
probabilidad, prediction = regresion.predict(x=x, theta=theta)
print(f'Testeo Prediccion')
print(f'\tx: {x}')
print(f'\ttheta utilizado: {regresion.theta}')
print(f'\tprobabilidad: {probabilidad}')
print(f'\tresultado: {prediction}')
# 5.1- grafico
def graph_prediction():
    graph_boundary()
    pl.plot(x[1], x[2], 'o:g',label='Prediccion')
scatter_plot(graph_prediction)

print(f'\n----------------------------------------------\n')

# 6.- desempeño
#6.1- separar los datos
training_data = data[0:80,:]
test_data = data[80:,:]
regresion = Regresion(training_data=training_data, test_data=test_data)
#6.2- optimizacion
costo, theta = regresion.optimize()
print(f'Optimizacion (80% training / 20% testing)')
print(f'\tTheta inicial: {theta_inicial}')
print(f'\tTheta minimo: {theta}')
print(f'\tCosto: {round(costo, 3)}')
#6.3- grafico
def graph_boundary2():
    # graph_boundary()
    x_boundary = np.array([np.min(training_data[:,1]), np.max(training_data[:,1])])
    y_boundary = -(theta[0] + theta[1]*x_boundary)/theta[2]
    pl.axline(x_boundary, y_boundary, color='mediumpurple' ,label='Limite de decision')
scatter_plot(graph_boundary2)
#6.4- rendimiento
recall, precision, fmeasure = regresion.perfomance()
print('Rendimiento (80% training / 20% testing)')
print(f'\trecall: {recall}')
print(f'\tprecision: {precision}')
print(f'\tf-measure: {fmeasure}')
#6,5- matriz confusion
print('\n-------------- Matriz de Confusion ---------------')
print(tabulate(
    [
        [0,regresion.true_negative, regresion.false_negative, round(precision, 3), recall, fmeasure],
        [1,regresion.false_positive, regresion.true_positive, round(precision, 3), recall, fmeasure],
        ['','','Promedio Total:', round(precision, 3), recall, fmeasure]
    ],
    headers = ['Y\YP', 0, 1, 'Precision', 'Recall', 'F-Measure'],
    # showindex=True,
    tablefmt='fancy_grid'
))
#>>>>>>> c7dbcd1b43cf04a0ca3532dfe5dd972a65c5d354
