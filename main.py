import math
import string
import random
from evolveLib import Evolving

def fitness(prog):
    target = "aaaaaaaaaaaaaaaaaaaaaaaa"
    value = 0
    bincount = 0
    
    for i in range(min(len(prog.out),len(target))):
        if not prog.out[i] == target[i]:
            value += 3

        if prog.out[i] in string.digits:
            bincount += 1
    value += bincount**2
            
    value += abs(len(prog.out) - len(target))**2

    if len(prog.code) > 4:
        value += ((len(prog.code) - 4)/2)**2

    return value

# Begin program
genSize = 100
keepRatio = 0.25
cutoff = math.floor(genSize*keepRatio)
timeLimit = 1

# Set last to [] if starting fresh
last = ['0100101100101001',
        '0100111000101001',
        '0100011000101001',
        '0100101100101001',
        '0100100100101001',
        '0100011100101001',
        '0100101100101001',
        '1110001010000110',
        '0100110100101001',
        '0100000100000101',
        '0100100000101001',
        '0100000000101001',
        '0100101100101001',
        '1111011010001100']

print('Generating initial population.')

if last == []:
    progspace = populate(genSize, fitness)
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
            print("gen " + str(t) + ': "' + newprogs[0].out + '", ' + str(newprogs[0].score))
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
    print(i.out)
    print('-----------------------------')

input('Press Enter to exit.')
