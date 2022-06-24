import numpy as np
from typing import Optional,Union
from misc import *

class Regresion:

    def __init__(self, data, theta=None, alpha=None):
        self.theta = np.array(theta) if theta else np.array(np.zeros(data.shape[1]))
        self.alpha = alpha or 0.01
        self.m = len(data)
        self.x = np.append(np.ones((self.m, 1)), np.reshape(np.array(data[:, 0]), (self.m, 1)), axis=1)
        self.y = np.array(data[:, 1])

        xs=np.linspace(-10,10,100)
        ys=np.linspace(-5,5,100)
        xx, yy = np.meshgrid(xs, ys)
        self.grid = {
            'costo': np.zeros((100, 100)),
            'x': xx,
            'y': yy,
        }
        self.historial = {
            'theta': [],
            'costo':[],
        }
        for index, v in np.ndenumerate(self.grid['costo']):
            self.grid['costo'][index] = self.costo([self.grid['x'][index],self.grid['y'][index]])
    
    def hipotesis(self, x, theta: Optional[np.array] = None):
        if type(x) != np.ndarray: x = np.array(x)
        if type(theta) != np.ndarray: theta = self.theta
        if x.shape != (2,): x = np.append([1], x)
        return np.sum(x.dot(self.theta))

    def costo(self, theta: Optional[Union[np.ndarray, list]] = None):
        # if type(theta) != np.ndarray: theta = self.theta
        if type(theta)!='NoneType':theta=np.array(theta)
        else: theta = self.theta
        return np.sum((self.x.dot(theta).transpose() - self.y)**2)/(2*self.m)

    def _calculo_gradiente(self, set_value: Optional[bool] = False, theta: Optional[np.array] = None):
        if type(theta) != np.ndarray: theta = self.theta
        _theta = np.array(theta)
        aux = self.x.dot(theta)
        
        for i in range(_theta.shape[0]):
            _theta[i] = float(_theta[i] - self.alpha*np.array((aux - self.y)*self.x[:, i]).sum()/self.m)
        costo = self.costo(_theta)
        if set_value:
            self.historial['costo'].append(costo)
            self.historial['theta'].append(_theta)
            self.theta = _theta
        return costo,_theta
    
    def normal(self):
        x_t = self.x.transpose()
        return np.linalg.inv(np.float_(x_t.dot(self.x))).dot(x_t).dot(self.y)