import numpy as np

class Reader:

    def __init__(self, path_file):
        with open(path_file, 'r') as f:
            self.raw = f.read().rstrip()
    
    def normalizar(self, data): # arreglar
        _data = np.array(data)
        x = _data[:,0]
        u = np.mean(x) # media aritmetica
        s = np.amax(x) # desviacion estandar
         
        for i in range(len(_data)):
            _data[i][0] = (_data[i][0]- u)/s
        return _data

    def txt_to_array(self, raw=None):
        if not raw: raw = self.raw
        #return np.array(map(lambda line:[ [float(value) for value in line.split(',')[:-1]], float(line.split(',')[-1]) ],raw.split('\n')))
        #return np.array([[np.array([float(value) for value in line.split(',')[:-1]]), float(line.split(',')[-1]) ] for line in raw.split('\n')], dtype=object)
        return np.array([[float(line.split(',')[0]), float(line.split(',')[1]) ] for line in raw.split('\n')], dtype=object)