import math
import string
import random
from evolveLib import Evolving
from vmengine import Program
numtostr = lambda x: Program.numtostr(x, Program.bits, False)

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
    length_out = len(''.join(i for i in prog.out if not i.isdigit()))
    length_code = len(prog.code)
    value -= length_out / length_code
    value -= length_out * 0.1
#    value += (prog.time / timeLimit) * 500000
    if prog.time > 0.99 * timeLimit: # kill programs that likely loop forever
        value = math.inf
    return value

# Set last to [] if starting fresh
#last = ['0100110001001101', '0100011001100101', '0100010111000001', '0100100110011001', '0100001101100101', '0100101111110101', '0100000001100101', '0101001111100110', '0100001011000101', '0100010101010001', '0100100010111101', '0100101001011001', '0100000011010001', '0100111101100001', '0100100001110001', '0100110010011001', '0100100011001001', '0100001101100001', '0100010011110001', '0100010011100101', '0100001001111001', '0100011001001101', '0100101001101001', '0100101111111101', '0100000111110001', '0100101011100101', '0100110110000001', '0100110101111101', '0100110110001001', '0100000110100001', '0100000100000101', '0100110001101101', '0100011111000101', '1010001111000011', '0100110011111101', '0100100100101101', '0100001011010101', '0100011100101001', '0100110110110101', '0100110010010001', '0100100100110001', '0100011110100101', '0100001000110001', '0100100001011101', '1100010000000011', '0110100110011000', '0000011001110000', '0100000101010101', '1111000000100111', '0100010101110101', '0100101011000001', '0100001101111101', '0100010111001001', '0100000110101101', '0100001001100100', '1000111110001000', '1110100111110101', '0100111110111101', '0000000011111001', '0100011110100101', '0100000101000001', '0110101100100101', '1100000010101111', '0100000010000101', '0100101110000101', '0100010011001001', '1111101111000101', '0100100111100001', '1101011100100010', '0111001000001111']
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
    print('[', end='')
    for num, instruction in enumerate(i.code, 1):
        print('"' + numtostr(instruction) + '"', end='')
        if num != len(i.code):
            print(', ', end='')
    print(']')

    print(i.out[:outputLimit], end = '')
    if len(i.out) > outputLimit:
        print('...', end = '')
    print('\n-----------------------------')

input('Press Enter to exit.')
