import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore

import pyqtgraph.opengl as gl

QtCore.QCoreApplication.setAttribute(QtCore.Qt.ApplicationAttribute.AA_ShareOpenGLContexts)

pg.mkQApp()

v1 = gl.GLViewWidget()
v1.show()
v1.addItem(gl.GLScatterPlotItem(pos=np.array([[1, 1, 1]])))
pg.exec()