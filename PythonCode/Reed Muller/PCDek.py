import itertools as it
import math
import random
import time
import sys
from HammingWeight import *
from RMParams import *
#####输出的是codeword 和infoword
def PCDek(r,m,cw, eras,DebugAusgabe=False):		###eras=0 表示eras个数为0,先转成二进制再看1的个数就是eras的个数
    n,k,d=RMParams(r, m)
    # n = 4
    # k = 3
    # Parity Check Dekodierer
    # Berechne Anzahl der Erasures.
    # Falls Anzahl >1, breche direkt ab und gebe zufaelliges PC-Codewort zurueck

    RestlicheEras = HammingWeight(eras)

    if (RestlicheEras>1):										##如果eras超过1个，则输出全零
        print ("Abbruch mit HW(eras) = ", RestlicheEras)
        return (0,0)
    else:
        # Berechne Hamming-Gewicht des Codeworts ohne Erasures
        tempcw = cw ^ (cw & eras)	## ^ means or
        # print ("Erasures: {:04b}".format(eras))
        # print ("Codeword: {:04b}".format(cw))
        # print ("tempcw  : {:04b}".format(tempcw))

        HammingCw = HammingWeight(tempcw)
        print ("HammingCW: ", HammingCw)

        if ((RestlicheEras==0) and ((HammingCw % 2) == 1)):		##如果没有eras且码字中奇数个1，则输出全零
            # Falls Anzahl der 1er ungerade und kein Erasure passiert ist, gebe zufaelliges Codewort zurueck,
            # da der PC-Code keinen Fehler korrigieren kann (maximal einen Erasure)
            #print ("Fall 1, Ausgabe: cw = {:04b}   ".format(0), " i = {:03b}".format(0))
            return (0,0)
        elif ((RestlicheEras==0) and ((HammingCw % 2) == 0)):	##如果没有eras且码字中偶数个1，说明无错，直接输出码字
            # Falls kein Erasure passiert ist und die Anzahl der 1er gerade ist, ist tempcw ein Codewort,
            # wird also unveraendert zurueckgegeben
            #print ("Fall 2: {:04b}".format(tempcw))
            return (tempcw, tempcw >> 1)        ###tempcw是最后判决后输出的codeword,tempcw>>是infocode
        else: # --> RestlicheEras == 1		##如果有一个eras且除去eras位后余下的码字中奇数个1，则翻转eras对应码字位的码字
            # Falls ein Erasure passiert ist, wird an der Stelle des Erasures eine 0 oder 1 gesetzt, um die
            # Anzahl der 1er gerade zu machen
            if ((HammingCw % 2) == 1):
                tempcw ^= eras
            #print ("Fall 3: {:04b}".format(tempcw))
            return (tempcw, tempcw >> 1)
    if DebugAusgabe:
        ausgabestr = "{0:0" + str(n) + "b}"
        print("RM({0}, {1}) - ".format(r,m) + "  PC-Dek: " + ausgabestr.format(tempcw) + " - " + ausgabestr.format(tempcw >> 1))