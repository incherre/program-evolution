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
last = ['0000001010011011', '0100111111011001', '0100111111100101', '0100101010000001', '0100100011010101', '0100110110001101', '0100001101110101', '0100101101100101', '0100010000111001', '0100000110010101', '0100011011100101', '0100101001110101', '0100111101011101', '0100111110000001', '0100001111001101', '0100010010011001', '0100010101100101', '1110111010111101', '0100101100010001', '0100000010011001', '0100010111111101', '0100010110001101', '0100110110101101', '0100000101010001', '0100101010100001', '0100100101001101', '0100110011110001', '0100001110101001', '1001110110110010', '0100011011101101', '0100110111100101', '0100011001110001', '0001010100101101', '0100001110010101', '0100001001110001', '0100110000101101', '0100111010101111', '0100011010011101', '1100100110010010', '0100111001100101', '1100100111000000', '0100000101001101', '0100111001011101', '0100011111110001', '0100110011000101', '0100010001111001', '0100101111101001', '0100011101011101', '0100100110101001', '0100101100100001', '0100111011010101', '0100001101100101', '0100101011000101', '0100111100101101', '0010010101010101', '0100011110110101', '0100000011001001', '0100000101011001', '0100100011100001', '0100001110011001', '1011000000111010', '0100011111001101', '0100010110000001', '0100000010011101', '0100011001011001', '0100001010110101', '0100101101010101', '0100000000000001', '1100001101100001', '0100000100011001', '0100111101111101', '1111011011010101']

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
