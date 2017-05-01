import itertools as it
import math
import random
import time
import sys
from GenPlotkin import *
from RMParams import *
from PCDek import *
from HammingWeight import *
from RepDek import *
def RekDek(r, m, cw, eras=0, DebugAusgabe=True):  ##r,m,cw,eras输入都是十进制,下面会转成2进制计算
    """                                            ##返回的是纠正后的码字和信息字
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
    (n, k, d) = RMParams(r, m)
    (nn, kk, dd) = RMParams(r - 1, m - 1)
    (nnn, kkk, ddd) = RMParams(r, m - 1)
    Paramstr = "({0:4d},".format(n) + " {0:3d},".format(k) + " {0:3d})".format(d)
    cw = cw & ((1 << n) - 1)
    ### Schritt 1)
    if r == 0:  ##如果是重复码，除去eras那些位后，判断余下的码字位1的个数，自减，小于0，判为1，反之，判为0
        # Repetition Dekodierung
        # Hamminggewicht unter Berücksichtigung von Erasures
        codeword, infoword = RepDek(r, m, cw, eras, DebugAusgabe=False)
        if DebugAusgabe:
            ausgabestr = "{0:0" + str(n) + "b}"
            print("RM({0}, {1}) - ".format(r, m) + Paramstr + " REP -> " + ausgabestr.format(cw) + ", hw=" + str(
                HammingWeight(cw)))
        return (codeword,infoword)
    if r == m - 1:
        # Parity Check Dekodierer
        tempcw,dekodiert = PCDek(r, m, cw, eras)
        if DebugAusgabe:
            ausgabestr = "{0:0" + str(n) + "b}"
            print("RM({0}, {1}) - ".format(r, m) + "  PC-Dek: " + ausgabestr.format(tempcw) + " - " + ausgabestr.format(
                dekodiert))
        return (tempcw, dekodiert)
    ### Schritt 2)
    # 2a) RM(r-1,m-1)
    n_halbe = 1 << (m - 1)          ###n_halbe等于2**(m-1),也就是值为n/2
    MaskeRechts = (1 << n_halbe) - 1    ###向左移n/2个长度单位后减一，得到的是全1，长度为n/2(低位)，可把高n/2位看作全0
    MaskeLinks = MaskeRechts << n_halbe ###(cw & MaskeRechts)得到的是：左半边为0，右半边为cw的后一半码字
                                        ###(cw  >> n_halbe)得到的是：左半边为0，右半边为cw的前一半码字，加起来总长度为n
    b_cw = (cw & MaskeRechts) ^ (cw >> n_halbe) ###cw >> n_halbe是RM(r,m)码字左半边,cw & MaskeRechts是码字右半边
    b_eras = (eras & MaskeRechts) | (eras >> n_halbe)   ##?? why is there | or

    (b, b_dek) = RekDek((r - 1), (m - 1), b_cw, b_eras) ###返回纠正后的码字和信息字     b是纠正后的RM(r-1,m-1)

    # 2b) a1 -> RM(r,m-1)RekDek     ###第一种情况
    a1_cw = (cw & MaskeRechts) ^ b  ###取前一半与纠正过的后一半异或的码字
    a1_eras = eras & MaskeRechts    ###eras为1时表示删除位，所以要或，不能异或，正常码字时eras是0

    (a1, a1_dek) = RekDek(r, (m - 1), a1_cw, a1_eras)

    # 2b) a2 -> RM(r,m-1)       ###第二种情况
    a2_cw = cw >> n_halbe       ###直接取前一半码字
    a2_eras = eras >> n_halbe

    (a2, a2_dek) = RekDek(r, (m - 1), a2_cw, a2_eras)

    if DebugAusgabe:
        if (a1_cw != a1):
            ausgabestr = "{0:0" + str(n_halbe) + "b}"
            print("a1 fehler " + "RM({0}, {1}) - ".format(r, m) + " : " + ausgabestr.format(
                a1_cw) + " - " + ausgabestr.format(a1))
        if (a2_cw != a2):
            ausgabestr = "{0:0" + str(n_halbe) + "b}"
            print("a2 fehler " + "RM({0}, {1}) - ".format(r, m) + " : " + ausgabestr.format(
                a2_cw) + " - " + ausgabestr.format(a2))
        if (b_cw != b):
            ausgabestr = "{0:0" + str(n_halbe) + "b}"
            print("b fehler " + "RM({0}, {1}) - ".format(r, m) + " : " + ausgabestr.format(
                b_cw) + " - " + ausgabestr.format(b))

    # 2d) kombiniere
    # Welches der neu bestimmten CWs a1, a2 ist näher am empfangenen CW?
    a1_distanz = 0
    a2_distanz = 0
    a1_cw = (a1 << n_halbe) | (a1 ^ b)
    a2_cw = (a2 << n_halbe) | (a2 ^ b)

    #  Berechne die Distanz:
    for i in range(n):
        aktbit = (1 << i)
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
        print("RM({0}, {1}) - ".format(r, m) + Paramstr + " Distanz -> {0} zu {1}".format(a1_distanz, a2_distanz))

    if (a1_distanz < a2_distanz):
        neu_cw = a1_cw
        a_dek = a1_dek
    else:
        neu_cw = a2_cw
        a_dek = a2_dek
    # Schritt 3
    if DebugAusgabe:
        if (a_dek > (1 << kk)):
            print("a dek zu lang" + "RM({0}, {1}) - ".format(r, m))
        if (b_dek > (1 << kkk)):
            print("bdek zu lang " + "RM({0}, {1}) - ".format(r, m))

    neu_dekodiert = ( a_dek << kk) | b_dek  ###之前为( b_dek << kk) | a_dek
    ausgabestr = "{0:0" + str(n) + "b}" ##设置ausgabestr长度为n的二进制
    if DebugAusgabe:
        print("RM({0}, {1}) - ".format(r, m) + "  Altes - neues CW : " + ausgabestr.format(
            cw) + " - " + ausgabestr.format(neu_cw))        ## ausgabestr.format（value）,将value转成长度为n的二进制字符串
        print("RM({0}, {1}) - ".format(r, m) + "  Fehler korrigiert: " + ausgabestr.format(cw ^ neu_cw))
    return (neu_cw, neu_dekodiert)
# binary_codeword=ausgabestr.format(neu_cw)
# binary_inforword=ausgabestr.format(neu_dekodiert)