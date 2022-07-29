import numpy as np
from scipy.optimize import minimize, fmin
from scipy.special import expit

class Regresion:

    def __init__(self, training_data, test_data=None, theta=None):
        self.training_data = np.array(training_data)
        self.training_y = np.reshape(training_data[:,3], (training_data.shape[0], 1)).T
        self.training_x = np.array(np.delete(arr=training_data, obj=3, axis=1))
        self.training_m = self.training_x.shape[0]

        if type(test_data) == np.ndarray:
            self.test_data = test_data
            self.test_y = np.reshape(test_data[:,3], (test_data.shape[0], 1)).T
            self.test_x = np.array(np.delete(arr=test_data, obj=3, axis=1))
            self.test_m = self.test_x.shape[0]
        self.theta = np.array(np.zeros(self.training_x.shape[1])) if not theta else np.array(theta) 

    def hipotesis(self, x, theta=None):
        if type(x) != np.ndarray: x = np.array(x)
        if type(theta) == list: theta=np.array(theta)
        if type(theta) != np.ndarray: theta = self.theta
        return expit(np.dot(theta, x.T))
    
    def cost(self, theta = None):
        if type(theta) == list:theta=np.array(theta)
        if type(theta) != np.ndarray: theta = self.theta
        x = self.training_x
        y = self.training_y
        m = self.training_m
        h = self.hipotesis(x=x, theta=theta)
        return -np.sum(y*np.log(h) + (1-y)*np.log(1-h))/(m)
    
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
        # self.__perfomance__()
        return result[1], result[0]
    
    def predict(self, x, theta = None):
        if type(theta) == list:theta=np.array(theta)
        if type(theta) != np.ndarray: theta = self.theta
        prob = np.sum(self.hipotesis(x=x, theta=theta))
        # return [prob, 1] if prob >= .5 else [prob, 0]
        return 1 if prob >= .5 else 0

    def perfomance(self):

        def decision_boundary(prob):
            return 1 if prob >= .5 else 0

        prediction = self.hipotesis(self.test_x)
        decision_boundary = np.vectorize(decision_boundary)
        prediction = np.reshape(decision_boundary(prediction).flatten(), (self.test_m, 1))
        result = np.hstack((self.test_y.T, prediction)).tolist()

        self.true_positive = len(list(filter(lambda row: row[0] == 1. and row[1] == 1., result)))
        self.false_positive = len(list(filter(lambda row: row[0] == 1. and row[1] == 0., result)))
        self.true_negative = len(list(filter(lambda row: row[0] == 0. and row[1] == 0., result)))
        self.false_negative = len(list(filter(lambda row: row[0] == 0. and row[1] == 1., result)))

        return [
            self.recall,
            self.precision,
            self.fmeasure
        ]
    
    @property
    def precision(self):
        return self.true_positive/(self.true_positive + self.false_positive)
    
    @property
    def recall(self):
        return self.true_positive/(self.true_positive + self.false_negative)
    
    @property
    def fmeasure(self):
        return 2*self.recall*self.precision/(self.recall+self.precision)