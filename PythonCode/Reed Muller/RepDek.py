from HammingWeight import *
from RMParams import *

def RepDek(r,m,cw, eras,DebugAusgabe=False):
    if r == 0:  ##如果是重复码，除去eras那些位后，判断余下的码字位1的个数，自减，小于0，判为1，反之，判为0
        # Repetition Dekodierung
        n,k,d = RMParams(r, m)
        Paramstr = "({0:4d},".format(n) + " {0:3d},".format(k) + " {0:3d})".format(d)
        Summe = 0
        if DebugAusgabe:
            ausgabestr = "{0:0" + str(n) + "b}"
            print("RM({0}, {1}) - ".format(r, m) + Paramstr + " REP -> " + ausgabestr.format(cw) + ", hw=" + str(
                HammingWeight(cw)))
        # Hamminggewicht unter Berücksichtigung von Erasures
        for i in range(1 << m):  ### i=[0,2**m-1]
            aktbit = (1 << i)  ### 1<<i == 1*2**i
            if not (aktbit & eras): ##左移i位后，该位置上对应的eras为0的话,若该位置上对应的cw为1，sum自减
                if (aktbit & cw):
                    Summe -= 1
                else:
                    Summe += 1
        if Summe < 0:
            tempcw = (1 << (1 << m)) - 1  ## m 位 全1
            return (tempcw, 1)  ##输出判决后的码字和信息字
        else:
            return (0, 0)   ##sum 大于等于0 时输出全0，相当于当0和1个数相等时，也判为0.