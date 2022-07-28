import numpy as np

class Reader:

    def __init__(self, path_file):
        data = np.loadtxt(path_file,delimiter=',',usecols=(0,1,2),unpack=True)
        x = np.transpose(np.array(data[:-1]))
        self.y = np.array(data[-1:])
        self.x = np.insert(x,0,1,axis=1)
        self.data = np.hstack((self.x, self.y.T))

    def get_data(self):
        return self.x, self.y

    def get_groups(self):
        group0 = self.data[np.in1d(self.data[:, 3], np.asarray([0.]))]
        group1 = self.data[np.in1d(self.data[:, 3], np.asarray([1.]))]
        return group0, group1