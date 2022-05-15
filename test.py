from Regresion import Regresion
from Reader import Reader
from misc import *
reader = Reader('data1.txt')
datos = reader.txt_to_array()
itr = 1500
alpha = 0.01

reg = Regresion(data=datos, alpha=alpha)
reg.gradiente(itr)
# print(f'Theta Gradiente: {reg.theta}')
# print(f'Theta Normal: {reg.normal()}')
print(f'Prediccion 35000 personas: {reg.hipotesis(3.5)}')
print(f'Prediccion 70000 personas: {reg.hipotesis(7)}')

# for i in range(itr):
#     costo,theta=reg._calculo_gradiente()
#     reg.theta=theta

# print(angle([1,reg.hipotesis(1)], [1,1]))
# print(angle([2, reg.hipotesis(2)], [1,1]))


print(degree([1,0], [0,1]))
for i in range(1500):
    print(degree([i, reg.hipotesis(i)], [0,1]))