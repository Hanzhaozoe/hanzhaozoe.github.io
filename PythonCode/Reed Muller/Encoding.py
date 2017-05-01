import itertools as it
import math
import random
import time
import sys
from GenPlotkin import *
from RMParams import *
####r,m,infocode 都是十进制输入
####返回的是十进制的codeword 和k位二进制的inforword
def Encoding(r,m,infocode):
    n, k, d = RMParams(r, m)
    ausgabestr = "{0:0" + str(k) + "b}"
    binary_infocode=ausgabestr.format(infocode)
    GeneratorMatrix = GenPlotkin(r, m)
    codeword=0
    for i in range(k):
        if int(binary_infocode[i]) == 1:
            codeword = codeword ^ GeneratorMatrix[i]
    return (codeword,binary_infocode)
# print(Encoding(r=1,m=4,infocode=1))
