import time
import math
import string

bits = 16
PC = 1
cmp = 2

def initializeRegisters():
    return [0] * bits

def strtonum(string, signed):
    #check if the string exists
    if len(string) <= 0:
        return 0
    
    #check if there is anything in string that is not a 0 or a 1
    for c in string:
        if not (c == '0' or c == '1'):
            return 0

    #convert
    num = int(string, 2)

    #deal with signedness
    if signed:
        num -= 2**(len(string) - 1)

    return num

def numtostr(num, length, signed):
    temp = num
    if signed:
        temp += 2 ** (length - 1)

    if temp < 0:
        temp = 0

    return bin(temp)[2:].zfill(length)[:length]

def none(inst, regs, out):
    pass

def add(inst, regs, out):
    reg1 = strtonum(inst[4:8], False)
    reg2 = strtonum(inst[8:12], False)
    dest = strtonum(inst[12:16], False)

    if dest > cmp: # some registers are read only
        regs[dest] = regs[reg1] + regs[reg2]

def sub(inst, regs, out):
    reg1 = strtonum(inst[4:8], False)
    reg2 = strtonum(inst[8:12], False)
    dest = strtonum(inst[12:16], False)

    if dest > cmp: # some registers are read only
        regs[dest] = regs[reg1] - regs[reg2]

def loadb(inst, regs, out):
    dest = strtonum(inst[12:16], False)
    bottom = inst[4:12]
    oldstring = numtostr(regs[dest], bits, False)
    newstring = oldstring[:8] + bottom

    if dest > cmp: # some registers are read only
        regs[dest] = strtonum(newstring, False)

def loadt(inst, regs, out):
    dest = strtonum(inst[12:16], False)
    top = inst[4:12]
    oldstring = numtostr(regs[dest], bits, False)
    newstring = top + oldstring[8:]

    if dest > cmp: # some registers are read only
        regs[dest] = strtonum(newstring, False)

def jump(inst, regs, out):
    jreg = strtonum(inst[12:16], False)
    offset = strtonum(inst[4:12], True)
    jumplocation = regs[jreg] + offset
    if jumplocation < 0:
        jumplocation = 0
    regs[PC] = jumplocation

def branch(inst, regs, out):
    offset = strtonum(inst[4:16], True)
    if regs[cmp] == 1:
        regs[PC] += offset
        if regs[PC] < 0:
            regs[PC] = 0

def eq(inst, regs, out):
    reg1 = strtonum(inst[4:8], False)
    reg2 = strtonum(inst[8:12], False)
    if regs[reg1] == regs[reg2]:
        regs[cmp] = 1
    else:
        regs[cmp] = 0

def lt(inst, regs, out):
    reg1 = strtonum(inst[4:8], False)
    reg2 = strtonum(inst[8:12], False)
    if regs[reg1] < regs[reg2]:
        regs[cmp] = 1
    else:
        regs[cmp] = 0

def gt(inst, regs, out):
    reg1 = strtonum(inst[4:8], False)
    reg2 = strtonum(inst[8:12], False)
    if regs[reg1] > regs[reg2]:
        regs[cmp] = 1
    else:
        regs[cmp] = 0

def no(inst, regs, out):
    if regs[cmp] == 1:
        regs[cmp] = 0
    else:
        regs[cmp] = 1

def prin(inst, regs, out):
    reg = strtonum(inst[4:8], False)
    offset = strtonum(inst[8:14], False)
    option = strtonum(inst[14:16], False)
    value = regs[reg] + offset
    
    if option == 1 and value >= 0 and value < len(string.printable):
        out['out'] += string.printable[value]
    elif option == 2:
        out['out'] += numtostr(value, bits, False)
    elif option == 3:
        out['out'] += numtostr(value, bits, True)
    else:
        out['out'] += str(value)

ops = {
    '0000': loadb,
    '0001': add,
    '0010': loadt,
    '0011': sub,
    '0100': prin,
    '0101': none,
    '0110': none,
    '0111': none,
    '1000': lt,
    '1001': gt,
    '1010': none,
    '1011': none,
    '1100': no,
    '1101': jump,
    '1110': eq,
    '1111': branch
    }

def runInstruction(inst, regs, out):
    opcode = inst[:4]
    ops[opcode](inst, regs, out)

def runProg(prog, timelimit):
    regs = initializeRegisters()
    starttime = time.time()
    out = {'out':''}

    while (timelimit > (time.time() - starttime) and regs[PC] < len(prog)):
        runInstruction(prog[regs[PC]], regs, out)
        regs[PC] += 1

    return out['out']
if __name__ == "__main__":
    testprog = [
    '0000011000110011',
    '0000000000010101',
    '0001010001010100',
    '0100010000000001',
    '1000010000110000',
    '1111011111111100'
    ]

    print(runProg(testprog, 10))
