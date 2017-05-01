#!/usr/bin/env python
#coding=utf8

"""
Modul zur Kodierung und Dekodierung von RM-Codes

Die rekursive version.
    Siehe:
    "On Error Correction for Physical Unclonable Functions"

Ludwig Kuerzinger
2014 TUM SEC
"""

import itertools as it
import math
import random
import time
import sys

#####################################################
## nützliche Funktionen

def HammingWeight(x): 
    w = 0
    while x:
        x &= x - 1
        w += 1
    return w

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



#####################################################
## Rekursiver - Dekodierer

def VerfolgeRekDekodiervorgang(r,m, TimingAnalyse=True, stand=''):
    """
    Beschreibt den Ablauf der Dekodierung mit dem rekursiven Dekodierer.
    Input:
        r, m   Parameter von RM(r,m)
        stand  interner Parameter zur Ablaufverfolgung
        NurGMC  Damit findet der Dekodierablauf so wie beim GMC statt
        TimingAnalyse   analysiert timing verhalten für Abschätzung bei der HW Implementierung, 
                        gibt ansonsten Zahl der Informationsbits zurück
    Output:
        Gibt beschreibenden Text zum Ablauf aus, sowie
        infbits: die Anzahl der zurückgegebenen Informationsbits
    """
    (n , k , d) = RMParams(r,m)
    (nn , kk , dd) = RMParams(r-1,m-1) # aus schritt 2a
    (nnn , kkk , ddd) = RMParams(r,m-1) # aus schritt 2b
    Paramstr = "({0:4d},".format(n) + " {0:3d},".format(k) + " {0:3d})".format(d)
    # Schritt 1)
    if r == 0:
        print(stand.ljust(30) +     "RM({0}, {1}) - ".format(r,m) + Paramstr + " -> Rep.")
        if TimingAnalyse:
            return 2*n
        else:         
            return k
    if r == m-1:
        print(stand.ljust(30) + "RM({0}, {1}) - ".format(r,m) + Paramstr + " -> PC")
        if TimingAnalyse:
            return 2*n
        else:         
            return k
    # Schritt 2a)
    print(stand.ljust(30) +         "RM({0}, {1}) - ".format(r,m) + Paramstr + " ." + "     -> c)  {0} + {1}".format(kk,kkk))
    infbits = VerfolgeRekDekodiervorgang(r-1, m-1, TimingAnalyse, stand + 'a) ')
    Timing = 3 * nn # zwei geladen, einer geschrieben
    # Schritt 2b)
    infbits = infbits + VerfolgeRekDekodiervorgang(r, m-1, TimingAnalyse, stand + 'b) ')
    Timing += 4* nn  # drei geladen, einer geschrieben
    # Schritt 3)
    if TimingAnalyse:
        return Timing + infbits
    else:
        return infbits


def RekDek(r, m, cw, eras=0, DebugAusgabe=True):		##r,m,cw,eras输入都是十进制,下面会转成2进制计算
    """
    Rekursiver Dekodieralgorithmus
    Input:
        r: r
        m: m
        codewort
        erasures
        DebugAusgabe -> Falls aktiv, gibt reichlich Debug-Informationen aus
    Output: 
        (schaetzung, inform)
        schaetzung -> das neue geschätzte Codewort
        inform  -> die dekodierten Informationsbits
    """
    # debug
    (n , k , d) = RMParams(r,m)
    (nn , kk , dd) = RMParams(r-1,m-1)
    (nnn , kkk , ddd) = RMParams(r,m-1)
    Paramstr = "({0:4d},".format(n) + " {0:3d},".format(k) + " {0:3d})".format(d)		### 4d是integer类型，十进制
    cw = cw & ( (1 << n) - 1 )
    ### Schritt 1)
    if r == 0:									##如果是重复码，除去eras那些位后，判断余下的码字位1的个数，自减，小于0，判为1，反之，判为0
        # Repetition Dekodierung
        Summe = 0
        if DebugAusgabe:
            ausgabestr = "{0:0" + str(n) + "b}"			##n位二进制
            print("RM({0}, {1}) - ".format(r,m) + Paramstr + " REP -> " + ausgabestr.format(cw) + ", hw="+str(HammingWeight(cw)))
        # Hamminggewicht unter Berücksichtigung von Erasures
        for i in range(1<<m):		### i=[0,2**m-1]
            aktbit = (1<<i)		### 1<<i == 1*2**i
            if not (aktbit & eras):
                if (aktbit & cw):
                    Summe -= 1
                else:
                    Summe += 1
        if Summe < 0:
            tempcw = (1 << (1<<m)) - 1
            return (tempcw, 1)			##输出判决后的码字
        else: 
            return (0,0)
    if r == m - 1 :
        # Parity Check Dekodierer
        tempcw = cw % (1 << n)
        tempcw = tempcw ^ (tempcw & eras) # Codewort ohne den Bits, auf denen ein Erasure gesetzt wurde.
        # Erster Durchgang. Hamminggewicht des CW ohne den erasures.
        HammingCw = HammingWeight( tempcw )
        # Parity Check OK?
        PCBit = ((HammingCw % 2) == 1)
        # Anzahl Erasures
        RestlicheEras = HammingWeight( eras )
        for i in reversed(list(range(n))):
            aktbit = (1<<i)
            if (aktbit & eras): # gibt es an dieser Stelle ein Erasure?
                if (RestlicheEras % 2) == 1: # Verbleibende Erasures ungerade
                    # Setze aktuelles CW-Bit
                    tempbit = cw & aktbit
                    tempcw |=  tempbit
                    if (tempbit > 0): # ist ein Bit gesetzt worden?
                        PCBit = not PCBit
                else: # Verbleibende Erasures ungerade
                    if PCBit:     # Setze PC-Bit
                        tempcw |= aktbit
                        PCBit = not PCBit
                RestlicheEras -= 1
            if (i == 0) and PCBit: # letztes Bit und noch immer PCBit gesetzt
                tempcw ^= 1
        dekodiert = (tempcw >> 1) % (1 << (n-1))
        if DebugAusgabe:
            ausgabestr = "{0:0" + str(n) + "b}"		##设置ausgabestr长度为n的二进制
            print("RM({0}, {1}) - ".format(r,m) + "  PC-Dek: " + ausgabestr.format(tempcw) + " - " + ausgabestr.format(dekodiert))
        return (tempcw, dekodiert)					## ausgabestr.format（value）,将value转成长度为n的二进制字符串
    ### Schritt 2)
    # 2a) RM(r-1,m-1)    
    n_halbe = 1 << (m - 1)					###n_halbe等于2**(m-1),也就是值为n/2
    MaskeRechts = (1 << n_halbe) - 1		###向左移n/2个长度单位后减一，得到的是全1，长度为n/2(低位)，可把高n/2位看作全0
    MaskeLinks = MaskeRechts << n_halbe			###(cw & MaskeRechts)得到的是：左半边为0，右半边为cw的后一半码字
												###(cw  >> n_halbe)得到的是：左半边为0，右半边为cw的前一半码字，加起来总长度为n
    b_cw =  (cw & MaskeRechts) ^ (cw  >> n_halbe)	### 码字前一半和后一半异或，得到RM(r-1,m-1)的码字 ^ XOR
    b_eras = (eras & MaskeRechts) | (eras  >> n_halbe)	### | OR  
    
    (b, b_dek) = RekDek((r-1), (m-1), b_cw, b_eras)
    
    # 2b) a1 -> RM(r,m-1)RekDek			###第一种情况
    a1_cw =  (cw & MaskeRechts) ^ b		###取前一半与纠正过的后一半异或的码字
    a1_eras = eras & MaskeRechts		###eras为1时表示删除位，所以要或，不能异或，正常码字时eras是0
    
    (a1, a1_dek) = RekDek(r, (m-1), a1_cw, a1_eras)
    
    # 2b) a2 -> RM(r,m-1)		###第二种情况
    a2_cw =  cw  >> n_halbe		###直接取前一半码字
    a2_eras = eras >> n_halbe

    (a2, a2_dek) = RekDek(r, (m-1), a2_cw, a2_eras)
    
    if DebugAusgabe:
        if (a1_cw != a1):
            ausgabestr = "{0:0" + str(n_halbe) + "b}"
            print("a1 fehler " + "RM({0}, {1}) - ".format(r,m) + " : " + ausgabestr.format(a1_cw) + " - " + ausgabestr.format(a1))
        if (a2_cw != a2):
            ausgabestr = "{0:0" + str(n_halbe) + "b}"
            print("a2 fehler " + "RM({0}, {1}) - ".format(r,m) + " : " + ausgabestr.format(a2_cw) + " - " + ausgabestr.format(a2))
        if (b_cw != b):
            ausgabestr = "{0:0" + str(n_halbe) + "b}"
            print("b fehler " + "RM({0}, {1}) - ".format(r,m) + " : " + ausgabestr.format(b_cw) + " - " + ausgabestr.format(b))

    # 2d) kombiniere
    # Welches der neu bestimmten CWs a1, a2 ist näher am empfangenen CW?
    a1_distanz = 0
    a2_distanz = 0
    a1_cw = (a1 << n_halbe) | (a1 ^ b)
    a2_cw = (a2 << n_halbe) | (a2 ^ b)
    
    #  Berechne die Distanz:
    for i in range(n): 
        aktbit = (1<<i)
        # <aktuelles Bit von CW> == <aktuelles Bit von a1> -> +0
        # <CW hat Erasure am aktuellen Bit> -> +1
        # <aktuelles Bit von CW> != <aktuelles Bit von a1> -> +2
        if not (aktbit & eras):
            if ((aktbit & cw) != (aktbit & a1_cw)):
                a1_distanz += 2
            if ((aktbit & cw) != (aktbit & a2_cw)):
                a2_distanz += 2
        else:
            a1_distanz += 1
            a2_distanz += 1
            
    if DebugAusgabe:
        print("RM({0}, {1}) - ".format(r,m) + Paramstr + " Distanz -> {0} zu {1}".format(a1_distanz , a2_distanz))
    
    if (a1_distanz < a2_distanz):
        neu_cw = a1_cw
        a_dek = a1_dek
    else:
        neu_cw = a2_cw
        a_dek = a2_dek
    # Schritt 3
    if DebugAusgabe:
        if (a_dek > (1 << kk)):
            print("a dek zu lang" +  "RM({0}, {1}) - ".format(r,m))
        if (b_dek > (1 << kkk)):
            print("bdek zu lang " +  "RM({0}, {1}) - ".format(r,m))
    
    neu_dekodiert = (b_dek << kk) | a_dek		##前面是RM(r-1,m-1)码字，后面是RM(r,m-1)码字，实际信息字的位置：应该从v0到vn,这里是从vn到v0.因为InverseI=True
    ausgabestr = "{0:0" + str(n) + "b}"
    if DebugAusgabe:
        print("RM({0}, {1}) - ".format(r,m) + "  Altes - neues CW : " + ausgabestr.format(cw) + " - " + ausgabestr.format(neu_cw))
        print("RM({0}, {1}) - ".format(r,m) + "  Fehler korrigiert: " + ausgabestr.format(cw ^ neu_cw))
    return (neu_cw, neu_dekodiert)


    
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
        rep = ((1 << n) - 1)	##1左移n位再减1，就是余下的位全是1，eg:n=7,2**7-1=127,n位全是1
        return [rep]
    if r == m-1:
        # Parity Check Matrix
        pc = list()
        for i in range(k):
            if InverseI: # Die Reihenfolge der Informationsbits sollte zu den im Kodierten gleich sein
                #  01
                #  10
                cw = 1 << i			## 单位阵上1的位置，每次向左移对应的i个单位,最后移k-1位
            else:
                #  10
                #  01
                cw = 1 << ((k-i)-1)	##和上面左移的单位反过来，最后移0位
            if ParityZuerst: # Parity Check bit hinten, sodass Dekodierung einfacher ist: >> 1  
                #  101			## 校验位在最后一位
                #  011
                cw = cw << 1	##cw 接着上面的移位后向左再移一位，多出来的最后一位补上1
                cw |= 1			##或 操作，最后一位补上1
            else:				## 校验位在第一位
                #  110
                #  101
				cw = cw << 1	#####修改了，增加项，之前没有这一句
                cw |= 1 << k 
            pc.append(cw)	##按十进制存储后，连起来的，pc里存的是十进制数字
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
        temp = doppeleintrag | (doppeleintrag << nnn)	##将RM(r,m-1)的生成矩阵左移nnn个单位后或上本身，相当于复制了一次
        clist.append(temp)
    clist.extend(alist)
    # Schritt 3)
    if Anfang:			###打印出RM(r,m)生成矩阵中每行对应的十进制值
        ausgabestr = "{0:0" + str(n) + "b}"	##设置ausgabestr长度为n的二进制
        print("RM({0}, {1}) - ".format(r,m)) ##输出十进制表示RM(r,m)，长度为1
        for uio in clist:
            print(ausgabestr.format(uio))		##输出uio，形式为：长度为n的二进制,即每行的十进制对应的二进制形式
    return clist		###打印出RM(r,m)生成矩阵

def KodPlotkin(r, m, x):
    """
    Plotkin - Kodierer für RM (r, 7)
    Input:
        x -> Informationsvektor, 
            Das LSB von x enspricht dem a0 der Input-Bits.
            Das MSB dementsprechend der untersten Zeile der Generatormatrix.
        r -> Parameter von RM(r,7)
    Output:
        128 bit L -> Codewort. LSB entspricht a0.
    """
    g = GenPlotkin(r, m, Anfang=False)
    temp_erg = 0
    temp_x = x
    # kodiere
    for xcv in g :
        if ((temp_x % 2) == 1):
            temp_erg ^=  xcv
        temp_x = temp_x >> 1
    return temp_erg

def Drucke_PlotkinMatrix(r,m=7):
    """
    Textausgabe der Plotkinmatrix für RM(r,m)
    """
    g = GenPlotkin(r, m, Anfang=False)
    n = 1 << m
    ausgabestr = "{0:0" + str(n) + "b}"
    for zeile in g:
        print(ausgabestr.format(zeile))



#####################################################
## RM 14 mit Plotkin Matrix und der std. Generatormatrix


# die Generator Matrix macht einen Unterschied.
# Zwar nicht in der Fehlerwahrscheinlichkeit, sondern in der Verkettung
# Siehe MesseHammingDistanzen()


def DekodierePlotkinRM14(c):
    """
    Dekodiere RM(1,4) ML Dekodierer, zweiter Versuch
    Input: 
        c -> empfangenes codewort
    Output:
        (dekodiert  , erasurebit , rest)
        dekodiert -> geschätzter Informationsvektor
        erasurebit
        rest -> Fehlervektor, oder: in welchem coset liegt c
    """
    CWListe = ErzeugeRekCwListeRM14()
    gefunden = False
    BisherBesteDistance = 17
    dekodiert = 0
    erasurebit = 1
    rest = 0
    # Teste jedes Codewort
    for i in range(2**5):
        # Berechne Hamming distance zu c, dem empfangenen CW
        AktuelleCoset = c ^ CWListe[i] # Kodiere i = 0..31
        distance = HammingWeight(AktuelleCoset)
        # zweites CW gefunden mit gleicher Distanz zum Empfangenen
        if distance == BisherBesteDistance : 
            gefunden = False
            erasurebit = 1
        # CW gefunden mit kleinerer Distanz zum Empfangenen
        elif distance < BisherBesteDistance :
            gefunden = True
            BisherBesteDistance = distance
            rest = AktuelleCoset
            dekodiert = i
            erasurebit = 0
    return (dekodiert  , erasurebit , rest)

#####################################################
## Optimierungs-Funktionen für das Simulationsmodul

def ErzeugeParamMatrix():
    mlist = list()
    for i in range(8):
        rlist = list()
        for j in range(i+1):
            rlist.append(RMParams(j,i))
        mlist.append(rlist)
    return pickle.dumps(mlist)
    
    
def ErzeugeGenMatrixMatrix():
    mlist = list()
    for i in range(8):
        rlist = list()
        for j in range(i):
            rlist.append(GenPlotkin(j, i, Anfang=False))
        mlist.append(rlist)
    return pickle.dumps(mlist)


def ErzeugeRekCwListeRM14():
    """
    Output:
        Liste aller Codewörter von RM(1,4)
    """
    codewortliste = list()
    for i in range(2**5):
        codewortliste.append( KodPlotkin(1, 4, i) )
    return (codewortliste)



def main():
    print(" Rekursiver Dekodierer für Reed-Muller Codes")
    print(" 2014, Ludwig Kürzinger, TUM, SEC")
    print(" Anwendungsbeispiel 1: Rekursiver Dekodierer, Dekodierablauf für RM(4,7)")
    input("ENTER zum Fortfahren. ")
    VerfolgeRekDekodiervorgang(4,7, NurGMC=False)
    print(" Anwendungsbeispiel 2: GMC Dekodierer, Dekodierablauf für RM(2,4)")
    input("ENTER zum Fortfahren. ")
    VerfolgeRekDekodiervorgang(2,4, NurGMC=True)
    print(" Anwendungsbeispiel 3: Plotkin-konstruierte Generatormatrix RM(2,5)")
    input("ENTER zum Fortfahren. ")
    Drucke_PlotkinMatrix(2,5)
    print(" Anwendungsbeispiel 4: Kodiere zufälliges Codeword mit zufälligen r,m mit Plotkin-Matrix")
    input("ENTER zum Fortfahren. ")
    m = random.randint(2,10)
    r = random.randint(0,m)
    (n,k,d) = RMParams(r,m)
    print("Code:  RM({0}, {1}) - ".format(r,m) +"({0:4d},".format(n) + " {0:3d},".format(k) + " {0:3d})".format(d))
    x = random.randint(0,2**k)
    kodiert = KodPlotkin(r, m, x)
    print("information:  "  + ("{0:0" + str(k) + "b}").format(x))
    print("Codewort   :  "  + ("{0:0" + str(n) + "b}").format(kodiert))

if __name__=='__main__':
    main()
    pass



def RepetitionDek(r,m, tempcw, eras):
    Summe = 0
    (n , k , d) = RMParams(r,m)
    # Hamminggewicht unter Berücksichtigung von Erasures
    for i in range(1<<m):
        aktbit = (1<<i)
        if (aktbit & eras):
            if (aktbit & tempcw):
                Summe -= 1
            else:
                Summe += 1
    if Summe < 0:
        tempcw = (1 << (1<<m)) - 1
        print (("{0:0" + str(n) + "b} , ").format(tempcw), 1)
    else: 
        print (("{0:0" + str(n) + "b} , ").format(tempcw), 0)


#####update  26.04.2017

