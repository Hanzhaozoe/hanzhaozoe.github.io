import numpy as np


def GenMa_RM(m):
    #Generatormatrix fuer einen R(1,m)-Code
    gm = np.empty(shape=(m + 1, pow(2, m)))
    gm[0] = 1
    for i in range(1, m + 1):
        for j in range(pow(2, i - 1)):
            gm[i, int((j * pow(2, m) / pow(2, i-1))):int((j * pow(2, m) / pow(2, i-1) + pow(2, m) / pow(2, i-1)))] = np.repeat(
                np.array([0, 1]), int((pow(2, m) / pow(2, i))))
    return gm
