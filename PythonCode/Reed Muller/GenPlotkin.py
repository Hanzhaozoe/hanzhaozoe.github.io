from RMParams import *

def GenPlotkin(r, m=7, Anfang=True, ParityZuerst=True, InverseI=False):	###InverseI 为True时,生成矩阵顺序倒一下,前面不为单位阵的形式
    """
    Generiere die Plotkin Matrix, passend zum rekursiven Dekodierer		###只适合递归译码，不适合GMC译码算法
    Bemerkungen: - diese Matrix passt nicht zum GMC-Dekodierer aus gmc.py
                 - PC-Matrix ist standartmäßig (I|1), kann aber mit den Parametern ParityZuerst und
                   InverseI verändert werden.
    Anfang -> Ist dieser gesetzt, wird die Generatormatrix in Textform ausgegeben
    """
    g = list()
    (n , k , d) = RMParams(r,m)
    Paramstr = "({0:4d},".format(n) + " {0:3d},".format(k) + " {0:3d})".format(d)
    # Schritt 1)
    if r == 0:
        # Rep
        rep = ((1 << n) - 1)
        return [rep]
    if r == m-1:
        # Parity Check Matrix
        pc = list()
        for i in range(k):
            if InverseI: # Die Reihenfolge der Informationsbits sollte zu den im Kodierten gleich sein
                #  01
                #  10
                cw = 1 << i
            else:
                #  10
                #  01
                cw = 1 << ((k-i)-1)
            if ParityZuerst: # Parity Check bit hinten, sodass Dekodierung einfacher ist: >> 1
                #  101
                #  011
                cw = cw << 1
                cw |= 1
            else:
                #  110
                #  101
                cw = cw << 1
                cw |= 1 << k
            pc.append(cw)
        return pc
    (nn , kk , dd) = RMParams(r-1,m-1) # aus schritt 2a
    (nnn , kkk , ddd) = RMParams(r,m-1) # aus schritt 2b
    # Schritt 2a) v
    alist =  GenPlotkin(r-1,m-1, False, ParityZuerst, InverseI)
    # Schritt 2b) u
    blist =  GenPlotkin(r,m-1, False, ParityZuerst, InverseI)
    # Schritt 2c)
    clist = list()
    for doppeleintrag in blist:
        temp = doppeleintrag | (doppeleintrag << nn)
        clist.append(temp)
    clist.extend(alist)
    # Schritt 3)
    if Anfang:			###打印出RM(r,m)生成矩阵中每行对应的十进制值
        ausgabestr = "{0:0" + str(n) + "b}"	##设置ausgabestr长度为n的二进制
        print("RM({0}, {1}) - ".format(r,m))
        for uio in clist:
            print(ausgabestr.format(uio))		##输出uio，形式为：长度为n的二进制
    return clist		###打印出RM(r,m)生成矩阵