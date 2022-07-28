import numpy as np
from scipy.optimize import minimize, fmin
from scipy.special import expit

class Regresion:

    def __init__(self, data, theta=None):
        self.x, self.y = data
        self.theta = np.array(np.zeros(self.x.shape[1])) if not theta else np.array(theta)
        self.m = len(self.x)

    def hipotesis(self, x, theta=None):
        if type(x) != np.ndarray: x = np.array(x)
        if type(theta) == list: theta=np.array(theta)
        if type(theta) != np.ndarray: theta = self.theta
        return expit(np.dot(theta, x.T))
    
    def cost(self, theta = None):
        if type(theta) == list:theta=np.array(theta)
        if type(theta) != np.ndarray: theta = self.theta
        h = self.hipotesis(x=self.x, theta=theta)
        return -np.sum(self.y*np.log(h) + (1-self.y)*np.log(1-h))/(self.m)
    
    def optimize(self, theta = None, save = True):
        if type(theta) == list:theta=np.array(theta)
        if type(theta) != np.ndarray: theta = self.theta
        _theta = np.array(theta)

        result = fmin(
            self.cost,
            x0=_theta,
            maxiter=400,
            full_output=True
            )
        if save: self.theta = result[0]
        return result[1], result[0]
    
    def predict(self, x, theta = None): #3.2.3 #arreglar porcentaje
        if type(theta) == list:theta=np.array(theta)
        if type(theta) != np.ndarray: theta = self.theta
        values = self.hipotesis(x=x, theta=theta)

        def decision_boundary(prob):
            return 1 if prob >= .5 else 0

        decision_boundary = np.vectorize(decision_boundary)
        prediction = np.reshape(decision_boundary(values).flatten(), (self.m, 1))
        total = prediction + self.y.T
        success = total[np.in1d(total, np.asarray([2.]))]
        return 100*len(success)/len(total)

    def performance(self, prediction, result): #3.3
        pass

        #recall, precision, f_measure

        # obtener 80% aleatorio de los datos para entrenamiento
        # el 20% restante es para perfomance