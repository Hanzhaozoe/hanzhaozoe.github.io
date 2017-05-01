import numpy as np
import math


def GenMaPlotkin(r, m):
    #Generatormatrix fuer einen R(r,m)-Code, die durch die Plotkin-Konstruktion erzeugt wird
    if r == 0:
        return np.array([np.ones(pow(2, m))])
    elif (m - r) == 1:
        k = pow(2, m) - 1
        a = np.eye(k)
        b = np.array([np.ones(k)])
        return np.concatenate((a, b.T), axis=1)
    else:
        a = GenMaPlotkin(r, m - 1)
        b = GenMaPlotkin(r - 1, m - 1)
        k1 = 0
        for i in range(0, r):
            temp1 = math.factorial(m - 1)			####order computation（m-1）!
            temp2 = math.factorial(i)
            temp3 = math.factorial(m - 1 - i)
            k1 += temp1 // (temp2 * temp3)
        e = np.zeros((k1, pow(2, m - 1)))			####compute the rows of matrix ZERO
        c1 = np.hstack([a, a])
        c2 = np.hstack([e, b])
        return np.vstack([c1, c2])		###vertical direction concatenation

