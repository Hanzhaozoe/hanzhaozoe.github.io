import math

def RMParams(r,m):
    n = 2**m
    d = 2**(m-r)
    k = 0
    i = 0
    if m == 0:
        return (1, 1, 0)
    for i in range(0,r+1):
        temp1 = math.factorial(m)
        temp2 = math.factorial(i)
        temp3 = math.factorial(m-i)
        k += temp1 // ( temp2 * temp3 )
    return (n, k, d)