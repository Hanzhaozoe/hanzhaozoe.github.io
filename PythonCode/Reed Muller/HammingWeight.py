def HammingWeight(x):
    w = 0
    while x:
        x &= x - 1
        w += 1
    return w
