import random
import math
import numpy as np
from GenMaPlotkin import *
from GMC_Algo_Simple import *
import hashlib
import binascii
r=1
m=4
n=pow(2,m)
d=pow(2,m-r)
t=math.floor((d-1)/2)

k1=0
for i in range(0, r+1):
    temp1 = math.factorial(m)  ####order computation（m-1）!
    temp2 = math.factorial(i)
    temp3 = math.factorial(m- i)
    k1 += temp1 // (temp2 * temp3)
k=k1        ### the number of information bits
A=GenMaPlotkin(r, m)        ###Generator matrix of RM(r,m)
s0= np.mat(np.random.randint(2, size=(1,k)),dtype=float)
print(s0)
u1=np.arange(n).reshape((1,n))
b= np.arange(n).reshape((1,n))
u1=np.mat((np.dot(s0,A))%2)
e0=np.mat(np.random.randint(2,size=(n,1)),dtype=float)
e0=e0.T
e1=e0
b=np.mat(b,dtype=float)
BPSK_b= np.mat(np.zeros(n),dtype=float)
mu, sigma = 0, 0.8
noise = np.mat(np.random.normal(mu, sigma, n),dtype=float)
received_codeword= np.mat(np.zeros(n),dtype=float)
for i in range(0,n):
    b[0,i]=(u1[0,i]+e0[0,i])%2
    if b[0,i] ==0:
        BPSK_b[0,i]=1
    else:
        BPSK_b[0,i]=-1
for i in range(0, n):
    received_codeword[0, i] = (b[0,i]+ e1[0,i])%2+ noise[0,i]
print(received_codeword)
print(noise)
c0=np.hstack((s0,b))
str_s0 = str(s0)
H_s0 = hashlib.sha3_256(str_s0.encode("utf-8"))
H_s0=H_s0.hexdigest()
str_s0b = str(c0)
H_s0b = hashlib.sha3_256(str_s0b.encode("utf8"))
H_s0b = H_s0b.hexdigest()
print(u1)







# for i in range(0,n):
#     b[0,i]=(u1[0,i]+e0[0,i])%2
#     if b[0,i] ==0:
#         BPSK_b[0,i]=1
#     else:
#         BPSK_b[0,i]=-1
#     received_codeword[0,i] =BPSK_b[0,i]+noise[0,i]
#     print(received_codeword[0,i])




# ################
# u2=(b+e1)%2
#
# codeward=GMC_Algo_Simple(r, m, u2)



