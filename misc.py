import numpy as np

def degree(vect1, vect2):
    a = np.array(vect1)
    b = np.array(vect2)

    inner = np.inner(a, b)
    norms = np.linalg.norm(a) * np.linalg.norm(b)

    cos = inner / norms
    rad = np.arccos(np.clip(cos, -1.0, 1.0))
    deg = np.rad2deg(rad)
    return deg

def around(array):
    arr = array.astype(float)
    np.round(a=arr, decimals=0, out=arr)
    return arr