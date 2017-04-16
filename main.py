import math
import string
import random
from evolveLib import Evolving

# Program options
genSize = 100
keepRatio = 0.25
cutoff = math.floor(genSize*keepRatio)
timeLimit = 1
outputLimit = 50

def fitness(prog):
    # This fitness function awards long output and punishes long programs
    # it is an attempt to evolve loops
    value = 0
    value -= len(''.join(i for i in prog.out if not i.isdigit())) * 2
    value += len(prog.code) ** 1.125
    if prog.time > 0.99 * timeLimit: # kill programs that likely loop forever
        value = math.inf
    return value

# Set last to [] if starting fresh
last = []

print('Generating initial population.')

if last == []:
    progspace = Evolving.populate(genSize, fitness)
else:
    progspace = [Evolving(last, fitness)]
    i = 0
    while i < (genSize - 1):
        progspace.append(progspace[i].mutateNew())
        i += 1
    
for prog in progspace:
    prog.evaluate(timeLimit)

print('Generated initial population. Updates will be issued as best score improves.')

t = 0
last = 0
try:
    while True:
        newprogs = sorted(progspace)[:cutoff] # sort the programs and take the first however many
        
        if not last == newprogs[0].score: # if the best score has changed, make note of it
            last = newprogs[0].score
            print("gen " + str(t) + ': "' + newprogs[0].out[:outputLimit], end = '')
            if len(newprogs[0].out) > outputLimit:
                print('...', end = '')
            print('", ' + str(newprogs[0].score))
        t += 1

        i = 0
        while len(newprogs) < genSize: # repopulate and evaluate
            tempProg = newprogs[i].mutateNew()
            tempProg.evaluate(timeLimit)
            newprogs.append(tempProg)
            i += 1

        progspace = random.sample(newprogs, len(newprogs)) #shuffle the programs

except KeyboardInterrupt:
    print("Interrupted by user around generation " + str(t))

best = sorted(progspace)[:5]

for i in best:
    print(str(i.code))
    print(i.out[:outputLimit], end = '')
    if len(i.out) > outputLimit:
        print('...', end = '')
    print('\n-----------------------------')

input('Press Enter to exit.')
