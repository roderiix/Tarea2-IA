from Reader import Reader
from Regresion import Regresion
import numpy as np

# empezar con objeto de clase regresion con set training al 100%, sin set de testeo
reader = Reader('ex2data1.txt')
data = reader.get_data()
# 1.- grafico dispersion

#hola
reg = Regresion(training_data=data)

# 2.- funcion sigmoidal
hipotesis = reg.hipotesis(x=[0,0,0])
print(f'hipotesis de x={[0,0,0]}: {hipotesis}')

# 3.- funcion costo
costo =reg.cost(theta=[0,0,0])
print(f'costo de x={[0,0,0]}: {costo}')

# 4.- optimizacion
costo, theta = reg.optimize(theta=[0,0,0])

    # costo
print(f'costo: {costo}')
print(f'Theta: {theta}')

    # grafico

# 5.- prediccion
prediction = reg.predict(x=[0,0,0], theta=theta)
    # valor
print(f'prediccion de x={[0,0,0]}: {prediction}')
    # grafico

# 6.- desempeño
training_data = data[np.random.choice(data.shape[0], 80, replace=False)]
    # separar datos por grupo (entrenamiento 80%, testeo 20%)
training_data = data[0:80,:]
test_data = data[80:,:]

        #crear otro objeto de la clase regresion, indicando ambos set de training y test
reg = Regresion(training_data=training_data, test_data=test_data)
    # entrenar

    # testear
    
        # recall

        # precision

        # fmeasure

    # matriz confusion