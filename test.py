from Regresion import Regresion
from Reader import Reader

reader = Reader('data1.txt')
datos = reader.txt_to_array()
#datos = reader.normalizar(datos)
itr = 1500
alpha = 0.01
#print(datos)

reg = Regresion(data=datos, alpha=alpha)
reg.gradiente(itr)
print(f'Theta Gradiente: {reg.theta}')
print(f'Theta Normal: {reg.normal()}')
print(f'Prediccion 35000 personas: {reg.hipotesis(35000)}')
print(f'Prediccion 70000 personas: {reg.hipotesis(70000)}')