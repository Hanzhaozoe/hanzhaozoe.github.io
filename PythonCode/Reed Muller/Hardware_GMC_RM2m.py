import operator
import numpy as np
from functools import reduce


class Stack:
    def __call__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)		####Add an item to the end of the list

    def pop(self):					####remove and return the last item in the list
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items) - 1]

    def size(self):
        return len(self.items)


def Hardware_GMC_RM2m(m, input):
    s = Stack()
    s.push(input)
    r = 2
    m1 = m
    for i_1 in range(m - r - 1):
        for i_2 in range(r - 1):
            y = s.pop()
            y1 = Schritt2a(y)
            s.push(y)
            s.push(y1)
        for i_3 in range(m1 - r - 1):
            y = s.pop()
            y1 = Schritt2a(y)
            s.push(y)
            s.push(y1)
            y1 = Repetition(s.pop())
            s.push(y1)
            y = s.pop()
            y1 = Schritt2b(s.pop(), y)
            s.push(y)
            s.push(y1)
        y1 = Parity_Check(s.pop())
        s.push(y1)
        for i_4 in range(m1 - r - 1):
            y1 = Schritt2c(s.pop(), s.pop())
            s.push(y1)
        y = s.pop()
        y1 = Schritt2b(s.pop(), y)
        s.push(y)
        s.push(y1)
        m1 -= 1
    y1 = Parity_Check(s.pop())
    s.push(y1)
    for i in range(m - r - 1):
        y1 = Schritt2c(s.pop(), s.pop())
        s.push(y1)
    return s.pop()


def Schritt2a(y):
    y1 = np.arange(y.size / 2, dtype='float64')
    for i in range(int(y1.size)):
        y1[i] = np.sign(y[2 * i] * y[2 * i + 1]) * min(np.abs(y[2 * i]), np.abs(y[2 * i + 1]))
    return (y1)


def Schritt2b(y, a1):
    y2 = np.arange(y.size / 2, dtype='float64')
    for i in range(int(y2.size)):
        y2[i] = 0.5 * (a1[i] * y[2 * i] + y[2 * i + 1])
    return (y2)


def Schritt2c(a2, a1):
    c = np.arange(2 * a1.size, dtype='float64')
    for i in range(int(c.size / 2)):
        c[2 * i] = a1[i] * a2[i]
        c[2 * i + 1] = a2[i]
    return c


def Parity_Check(y):
    c = np.array([])
    for i in range(int(y.size)):
        ct = np.sign(y[i])
        # Betreuer fragen für Fall ct =0
        if ct == 0:
            ct = 1
        c = np.hstack((c, [ct]))
    if prod(c) == -1:
        s = np.where(np.fabs(y) == min(np.fabs(y)))
        c[s] = -c[s]
    return c


def Repetition(y):
    ct = np.sign(sum(y))
    if ct == 0:
        ct = 1
    c = np.array([])
    for i in range(int(y.size)):
        c = np.hstack((c, [ct]))
    return c


def prod(i):
    return reduce(operator.mul, i, 1)
