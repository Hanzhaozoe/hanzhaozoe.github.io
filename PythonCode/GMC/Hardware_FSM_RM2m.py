import operator
import numpy as np
from functools import reduce


def prod(i):
    #Hilfsfunktion
    return reduce(operator.mul, i, 1)


class Stack:
    #Definition einer Stack Klasse
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items) - 1]

    def size(self):
        return len(self.items)


class InitializationError(Exception): pass


class StateMachine:
    #Definition eienr State Machine Klasse
    def __init__(self):
        self.handlers = {}
        self.startState = None
        self.endStates = []

    def add_state(self, name, handler, end_state=0):
        name = name.upper()
        self.handlers[name] = handler
        if end_state:
            self.endStates.append(name)

    def set_start(self, name):
        self.startState = name.upper()

    def run(self, cargo1, cargo2):
        try:
            handler = self.handlers[self.startState]
        except:
            raise InitializationError("must call .set_start() before .run()")
        if not self.endStates:
            raise InitializationError("at least one state must be an end_state")

        while True:
            (newState, cargo1, cargo2) = handler(cargo1, cargo2)
            if newState.upper() in self.endStates:
                print("reached ", newState, cargo1)
                break
            else:
                handler = self.handlers[newState.upper()]


class Counter:
    #Hier wird eine Klasse fuer die Counter erstellt
    #Fester Parameter r:
    r = 2
    m1 = 0
    # Fuer Counter extra_runde:
    cer1 = 0
    cer2 = 0
    extra_runde = 0
    # Fuer Counter right_done:
    crd = 0
    right_done = 0
    # Fuer Counter final_up:
    cfu = 0
    final_up = 0
    # Fuer Counter left_done:
    cld = 1
    left_done = 0
    # Fuer Counter ready_for_rp:
    crfrp = r
    ready_for_rp = 0
    # Fuer Counter rauf_done:
    crad = 0
    rauf_done = 0
    # Fuer Counter runter_done:
    crud = 0
    runter_done = 0

    def __init__(self, m):
        self.items = []
        # Bei der Initialisierung des Counters wird m gesetzt:
        self.crd = m - self.r
        self.crud = m - self.r - 1
        self.m1 = m


    def set_counter(self, extra_ru, minus_ru, right_d, going_up, rauf_fertig, ready_rp, rep_d, rauf_d, runter_d, extra_c):
        #Diese Funktion ruft alle Counter auf
        self.counter_extra_runde(extra_ru, minus_ru, extra_c)
        self.counter_right_done(right_d)
        self.counter_final_up(right_d, going_up)
        self.counter_left_done(rauf_fertig)
        self.counter_ready_for_rp(ready_rp, right_d)
        self.counter_rauf_done(rep_d, rauf_d)
        self.counter_runter_done(runter_d, rauf_fertig)

    def counter_extra_runde(self, extra_ru, minus_ru, extra_c):
        #Counter extra_runde
        if extra_ru == 1:
            self.cer1 += 1
        if extra_c == 1:
            self.cer2 = self.cer1
        if minus_ru == 1:
            self.cer2 -= 1
        if self.cer2 == 0:
            self.extra_runde = 1
        else:
            self.extra_runde = 0

    def counter_right_done(self, right_d):
        #Counter right_done
        if right_d == 1:
            self.crd -= 1
        if self.crd == 0:
            self.right_done = 1
        else:
            self.right_done = 0

    def counter_final_up(self, right_d, going_up):
        #Counter final_up
        if (right_d == 1) & (self.left_done == 1):
            self.cfu += 1
        if going_up == 1:
            self.cfu -= 1
        if self.cfu == 0:
            self.final_up = 1
        else:
            self.final_up = 0

    def counter_left_done(self, rauf_fertig):
        #Counter left_done
        if rauf_fertig == 1:
            self.cld -= 1
        if self.cld == 0:
            self.left_done = 1

    def counter_ready_for_rp(self, ready_rp, right_d):
        #Counter ready_for_rp
        if (ready_rp == 1) & (self.crfrp != 0):
            self.crfrp -= 1
        if right_d == 1:
            self.crfrp = self.r
        if self.crfrp == 0:
            self.ready_for_rp = 1
        else:
            self.ready_for_rp = 0

    def counter_rauf_done(self, rep_d, rauf_d):
        #Counter rauf_done
        if rep_d == 1:
            self.crad += 1
        if rauf_d == 1:
            self.crad -= 1
        if self.crad == 0:
            self.rauf_done = 1
        else:
            self.rauf_done = 0

    def counter_runter_done(self, runter_d, rauf_fertig):
        #Counter runter_done
        if runter_d == 1:
            self.crud -= 1
        if rauf_fertig == 1:
            self.crud = self.m1 - self.r - 1
        if self.crud == 0:
            self.runter_done = 1
        else:
            self.runter_done = 0


def begin_transition(input, m):
    #Uebergangslogik Fuer den Zustand Begin
    print("begin") #Zeigt den aktuellen Zustand an. Kann rausgenommen werden.
    s = Stack()
    c = Counter(m)
    input = np.array(input)
    s.push(input)
    newState = "start_state"
    return(newState, s, c)


def start_transition(s, c):
    #Uebergangslogik Fuer den Zustand Start
    print("start") #Zeigt den aktuellen Zustand an. Kann rausgenommen werden.
    # right_d=1 und exrta_c=1
    c.set_counter(0, 0, 1, 0, 0, 0, 0, 0, 0, 1)
    if c.left_done == 0:
        newState = "links_state"
    else:
        newState = "extra_state"
    return(newState, s, c)


def links_transition(s, c):
    #Uebergangslogik Fuer den Zustand Links
    print("links") #Zeigt den aktuellen Zustand an. Kann rausgenommen werden.
    # ready_rp=1
    c.set_counter(0, 0, 0, 0, 0, 1, 0, 0, 0, 0)
    y = s.pop()
    y1 = np.arange(y.size / 2, dtype='float64')
    for i in range(int(y1.size)):
        y1[i] = np.sign(y[2 * i] * y[2 * i + 1]) * min(np.abs(y[2 * i]), np.abs(y[2 * i + 1]))
    s.push(y)
    s.push(y1)
    if c.ready_for_rp == 1:
        newState = "repetition_state"
    else:
        newState = "links_state"
    return(newState, s, c)



def extra_transition(s, c):
    #Uebergangslogik Fuer den Zustand Extra
    print("extra")  #Zeigt den aktuellen Zustand an. Kann rausgenommen werden.
    # minus_ru=1 und runter_d=1
    c.set_counter(0, 1, 0, 0, 0, 0, 0, 0, 1, 0)
    if c.extra_runde == 1:
        newState = "rechts_state"
    else:
        newState = "extra_state"
    return(newState, s, c)


def repetition_transition(s, c):
    #Uebergangslogik Fuer den Zustand Repetition
    print("repetition")  #Zeigt den aktuellen Zustand an. Kann rausgenommen werden.
    # rep_d=1
    c.set_counter(0, 0, 0, 0, 0, 0, 1, 0, 0, 0)
    y = s.pop()
    ct = np.sign(sum(y))
    if ct == 0:
        ct = 1
    y1 = np.array([])
    for i in range(int(y.size)):
        y1 = np.hstack((y1, [ct]))
    s.push(y1)
    newState = "runter_state"
    return (newState, s, c)


def rechts_transition(s, c):
    #Uebergangslogik Fuer den Zustand Rechts
    print("rechts")  #Zeigt den aktuellen Zustand an. Kann rausgenommen werden.
    c.set_counter(0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    a1 = s.pop()
    y = s.pop()
    y1 = np.arange(y.size / 2, dtype='float64')
    for i in range(int(y1.size)):
        y1[i] = 0.5 * (a1[i] * y[2 * i] + y[2 * i + 1])
    s.push(a1)
    s.push(y1)
    if c.right_done == 1:
        newState = "parity_check_state"
    else:
        newState = "links_state"
    return (newState, s, c)


def runter_transition(s, c):
    #Uebergangslogik Fuer den Zustand Runter
    print("runter")  #Zeigt den aktuellen Zustand an. Kann rausgenommen werden.
    # runter_d=1
    c.set_counter(0, 0, 0, 0, 0, 0, 0, 0, 1, 0)
    a1 = s.pop()
    y = s.pop()
    y1 = np.arange(y.size / 2, dtype='float64')
    for i in range(int(y1.size)):
        y1[i] = 0.5 * (a1[i] * y[2 * i] + y[2 * i + 1])
    s.push(a1)
    s.push(y1)
    if c.runter_done == 1:
        newState = "parity_check_state"
    else:
        newState = "links_state"
    return (newState, s, c)


def parity_check_transition(s, c):
    #Uebergangslogik Fuer den Zustand Parity-Check
    print("parity_check")  #Zeigt den aktuellen Zustand an. Kann rausgenommen werden.
    c.set_counter(0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    y = s.pop()
    y1 = np.array([])
    for i in range(int(y.size)):
        ct = np.sign(y[i])
        # Betreuer fragen Fuer Fall ct =0
        if ct == 0:
            ct = 1
        y1 = np.hstack((y1, [ct]))
    if prod(y1) == -1:
        s = np.where(np.fabs(y) == min(np.fabs(y)))
        y1[s] = -y1[s]
    s.push(y1)
    if c.right_done == 1:
        newState = "up_state"
    else:
        newState = "rauf_state"
    return (newState, s, c)


def rauf_transition(s, c):
    #Uebergangslogik Fuer den Zustand Rauf
    print("rauf")  #Zeigt den aktuellen Zustand an. Kann rausgenommen werden.
    # rauf_d=1
    c.set_counter(0, 0, 0, 0, 0, 0, 0, 1, 0, 0)
    a2 = s.pop()
    a1 = s.pop()
    y1 = np.arange(2 * a1.size, dtype='float64')
    for i in range(int(y1.size / 2)):
        y1[2 * i] = a1[i] * a2[i]
        y1[2 * i + 1] = a2[i]
    s.push(y1)
    if c.rauf_done == 1:
        newState = "rauf_fertig_state"
    else:
        newState = "rauf_state"
    return (newState, s, c)


def rauf_fertig_transition(s, c):
    #Uebergangslogik Fuer den Zustand Rauf_Fertig
    print("rauf_fertig")  #Zeigt den aktuellen Zustand an. Kann rausgenommen werden.
    # rauf_fertig=1 und extra_ru=1
    c.set_counter(1, 0, 0, 0, 1, 0, 0, 0, 0, 0)
    newState = "start_state"
    return (newState, s, c)


def up_transition(s, c):
    #Uebergangslogik Fuer den Zustand Up
    print("up")  #Zeigt den aktuellen Zustand an. Kann rausgenommen werden.
    # going_d=1
    c.set_counter(0, 0, 0, 1, 0, 0, 0, 0, 0, 0)
    a2 = s.pop()
    a1 = s.pop()
    y1 = np.arange(2 * a1.size, dtype='float64')
    for i in range(int(y1.size / 2)):
        y1[2 * i] = a1[i] * a2[i]
        y1[2 * i + 1] = a2[i]
    s.push(y1)
    if c.final_up == 1:
        newState = "end_state"
        return(newState, s.pop(), "")
    else:
        newState = "up_state"
        return (newState, s, c)


#Initialisierung der state machine:
if __name__== "__main__":
    m = StateMachine()
    m.add_state("begin_state", begin_transition)
    m.add_state("start_state", start_transition)
    m.add_state("extra_state", extra_transition)
    m.add_state("rechts_state", rechts_transition)
    m.add_state("links_state", links_transition)
    m.add_state("repetition_state", repetition_transition)
    m.add_state("runter_state", runter_transition)
    m.add_state("parity_check_state", parity_check_transition)
    m.add_state("up_state", up_transition)
    m.add_state("rauf_state", rauf_transition)
    m.add_state("rauf_fertig_state", rauf_fertig_transition)
    m.add_state("end_state", None, end_state=1)
    m.set_start("begin_state")
    #Naechster Befehl startet den Algorithmus Fuer c und m1
    #m.run(c, m1)

