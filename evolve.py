import random
import math
import string
import vmengine

chance0 = 0.08
chance1 = 0.1
chance2 = 0.01
chance3 = 0.008

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

def mutate(prog):
    l = []
    for i in range(len(prog)):
        if random.random() < chance3:
            #take one away
            pass
        elif random.random() < chance1:
            #change it a bit
            l.append(change(prog[i]))
        else:
            #plain copy
            l.append(prog[i])
            
        if random.random() < chance2:
            #add a new one
            l.append(randomBits(16))
    return l

def newprog(length):
    l = []
    for i in range(length):
        l.append(randomBits(16))
    return l

def populate(number, length):
    l = []
    for i in range(number):
        l.append({'prog':newprog(length),'out':'','score':1000})
    return l

def evaluate(thing):
    target = "aaaaaaaaaaaaaaaaaaaaaaaa"
    value = 0
    bincount = 0
    
    for i in range(min(len(thing['out']),len(target))):
        if not thing['out'][i] == target[i]:
            value += 3

        if thing['out'][i] in string.digits:
            bincount += 1
    value += bincount**2
            
    value += abs(len(thing['out']) - len(target))**2

    if len(thing['prog']) > 4:
        value += ((len(thing['prog']) - 4)/2)**2

    return value

def getkey(thing):
    return thing['score']

# Begin program
genSize = 100
keepRatio = 0.25
cutoff = math.floor(genSize*keepRatio)

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

if last == []:
    progspace = populate(genSize, 4)
else:
    progspace = [{'prog':last,'out':'','score':1000}]
    i = 0
    while len(progspace) < genSize:
        tempProg = mutate(progspace[i]['prog'])
        progspace.append({'prog':tempProg,'out':'','score':1000})
        i += 1
    
for prog in progspace:
    prog['out'] = vmengine.runProg(prog['prog'], 1)
    prog['score'] = evaluate(prog)

print('Generated initial population. Updates will be issued as best score improves.')

t = 0
last = 0
try:
    while True:
        newprogs = sorted(progspace, key=getkey)[:cutoff]
        
        if not last == newprogs[0]['score']:
            last = newprogs[0]['score']
            print("gen " + str(t) + ': "' + newprogs[0]['out'] + '", ' + str(newprogs[0]['score']))
        t += 1

        i = 0
        while len(newprogs) < genSize:
            tempProg = mutate(newprogs[i]['prog'])
            tempOut = vmengine.runProg(tempProg, 1)
            tempScore = evaluate({'prog':tempProg,'out':tempOut})
            
            newprogs.append({'prog':tempProg,'out':tempOut,'score':tempScore})
            i += 1

        progspace = random.sample(newprogs, len(newprogs))

except KeyboardInterrupt:
    print("Interrupted by user around generation " + str(t))
    pass

best = sorted(progspace, key=getkey)[:5]

for i in best:
    print(str(i['prog']))
    print(i['out'])
    print('-----------------------------')
