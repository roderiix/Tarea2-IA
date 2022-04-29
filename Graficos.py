from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

class Graficos:
    def grafico1(self,dato1,dato2):
        figure = plt.figure()
        plt.title("Figura 1:Diagrama de dispersión de datos de entrenamiento")
        plt.ylabel("Beneficios en 10miles")
        plt.xlabel("Poblacion en 10miles")
        plt.plot(dato1,dato2,"x",markersize=2.5)
        plt.grid()
        plt.show()