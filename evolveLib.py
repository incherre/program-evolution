import random
import math

from vmengine import Program

chance0 = 0.08
chance1 = 0.1
chance2 = 0.01
chance3 = 0.008
defaultLength = 5

class Evolving(Program):
    '''This class allows regular programs to be mutated and evaluated.'''
    
    def __init__(self, code, fitness):
        if code == []:
            Program.__init__(self, Evolving.newCode())
        else:
            Program.__init__(self, code)
        
        # fitness is a function taking an Evolving object
        # and returning a number, smaller is better
        self.fitness = fitness
        self.score = math.inf

    def evaluate(self, timeLimit):
        self.runProgram(timeLimit)
        self.score = self.fitness(self)

    def mutateNew(self):
        l = []
        for i in range(len(self.code)):
            if random.random() < chance3:
                #take one away
                pass
            elif random.random() < chance1:
                #change it a bit
                l.append(Evolving.change(self.code[i]))
            else:
                #plain copy
                l.append(self.code[i])
                
            if random.random() < chance2:
                #add a new one
                l.append(Evolving.randomBits(Program.bits))
        return Evolving(l, self.fitness)

    def newCode(length=defaultLength):
        l = []
        for i in range(length):
            l.append(Evolving.randomBits(Program.bits))
        return l

    def randomBits(n):
        s = ''
        for i in range(n):
            s += random.choice(['0', '1'])
        return s

    def change(s):
        o = ''
        for c in s:
            if random.random() < chance0:
                o += random.choice(['0', '1'])
            else:
                o += c
        return o

    def populate(number, fitness):
        l = []
        for i in range(number):
            l.append(Evolving([], fitness))
        return l

    def __lt__(self, other):
        return self.score < other.score
