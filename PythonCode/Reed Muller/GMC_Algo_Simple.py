import operator
import numpy as np
from functools import reduce

def prod(i):
    #Hilfsfunktion
    return reduce(operator.mul, i, 1)	####operator.mul -----return the product of i * 1, iteration is from left to right

def GMC_Algo_Simple(r, m, y):
    # Der klssische rekursive GMC-Algorithmus
    # Uebergabeparameter: r und m aus R(r,m) und Input-Vektor y
    y = np.array(y)
    if r == 0:
        ct = np.sign(sum(y))
        if ct == 0:
            ct = 1
        c = np.array([])
        for i in range(int(y.size)):
            c = np.hstack((c, [ct]))
        return c
    elif (m - r) == 1:
        c = np.array([])
        for i in range(int(y.size)):
            ct = np.sign(y[i])
            if ct == 0:
                ct = 1
            c = np.hstack((c, [ct]))
        if prod(c) == -1:
            s = np.where(np.fabs(y) == min(np.fabs(y)))		###np.fabs  return the absolute value
            c[s] = -c[s]
        return c
    else:
        y1 = np.arange(y.size/2, dtype='float64')
        for i in range(int(y1.size)):
            y1[i] = np.sign(y[2*i]*y[2*i+1])*min(np.abs(y[2*i]),np.abs(y[2*i+1]))
        a1 = GMC_Algo_Simple(r-1, m-1, y1)
        y2 = np.arange(y1.size, dtype='float64')
        for i in range(int(y2.size)):
            y2[i] = 0.5*(a1[i]*y[2*i]+y[2*i+1])
        a2 = GMC_Algo_Simple(r, m-1, y2)
        c = np.arange(y.size, dtype='float64')
        for i in range(int(c.size/2)):
            c[2*i] = a1[i]*a2[i]
            c[2*i+1] = a2[i]
        return c
