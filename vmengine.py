import time
import math
import string

class Program:
    'A class representing a particular program to be run on the VM'
    
    bits = 16
    PC = 1
    cmp = 2
    
    def __init__(self, code):
        self.code = []
        for instruction in code:
            if type(instruction) != int:
                self.code.append(int(instruction, base=2))
            else:
                self.code.append(instruction)
 
    def runProgram(self, timelimit):
        self.regs = Program.initializeRegisters()
        self.out = ''
        startTime = time.time()

        while (timelimit >= (time.time() - startTime) and self.regs[Program.PC] < len(self.code)):
            self.runInstruction(self.code[self.regs[Program.PC]])
            self.regs[Program.PC] += 1

        self.time = time.time() - startTime

    def runInstruction(self, inst):
        ops = [
            self.loadb,
            self.add,
            self.loadt,
            self.sub,
            self.prin,
            self.none,
            self.none,
            self.none,
            self.lt,
            self.gt,
            self.none,
            self.none,
            self.no,
            self.jump,
            self.eq,
            self.branch
        ]
        mask = 15 << 12
        opcode = (inst & mask) >> 12
        ops[opcode](inst)

    def prin(self, inst):
        reg = Program.extract(inst, self.bits, 4, 8, False)
        offset = Program.extract(inst, self.bits, 8, 14, False)
        option = Program.extract(inst, self.bits, 14, 16, False)
        value = self.regs[reg] + offset
    
        if option == 1 and value >= 0 and value < len(string.printable):
            self.out += string.printable[value]
        elif option == 2:
            self.out += Program.numtostr(value, Program.bits, False)
        elif option == 3:
            self.out += Program.numtostr(value, Program.bits, True)
        else:
            self.out += str(value)

    def no(self, inst):
        if self.regs[Program.cmp] == 1:
            self.regs[Program.cmp] = 0
        else:
            self.regs[Program.cmp] = 1

    def gt(self, inst):
        reg1 = Program.extract(inst, self.bits, 4, 8, False)
        reg2 = Program.extract(inst, self.bits, 8, 12, False)
        if self.regs[reg1] > self.regs[reg2]:
            self.regs[Program.cmp] = 1
        else:
            self.regs[Program.cmp] = 0

    def lt(self, inst):
        reg1 = Program.extract(inst, self.bits, 4, 8, False)
        reg2 = Program.extract(inst, self.bits, 8, 12, False)
        if self.regs[reg1] < self.regs[reg2]:
            self.regs[Program.cmp] = 1
        else:
            self.regs[Program.cmp] = 0

    def eq(self, inst):
        reg1 = Program.extract(inst, self.bits, 4, 8, False)
        reg2 = Program.extract(inst, self.bits, 8, 12, False)
        if self.regs[reg1] == self.regs[reg2]:
            self.regs[Program.cmp] = 1
        else:
            self.regs[Program.cmp] = 0

    def branch(self, inst):
        offset = Program.extract(inst, self.bits, 4, 16, True)
        if self.regs[Program.cmp] == 1:
            self.regs[Program.PC] += offset
            if self.regs[Program.PC] < 0:
                self.regs[Program.PC] = 0

    def jump(self, inst):
        jreg = Program.extract(inst, self.bits, 12, 16, False)
        offset = Program.extract(inst, self.bits, 4, 12, True)
        jumplocation = self.regs[jreg] + offset
        if jumplocation < 0:
            jumplocation = 0
        self.regs[Program.PC] = jumplocation

    def loadt(self, inst):
        dest = Program.extract(inst, self.bits, 12, 16, False)
        top = Program.extract(inst, self.bits, 4, 12, False)
        oldnum = self.regs[dest]
        newnum = top << (self.bits // 2) | (oldnum & ((1 << (self.bits // 2)) - 1))

        if dest > Program.cmp: # some registers are read only
            self.regs[dest] = newnum

    def loadb(self, inst):
        dest = Program.extract(inst, self.bits, 12, 16, False)
        bottom = Program.extract(inst, self.bits, 4, 12, False)
        oldnum = self.regs[dest]
        newnum = bottom | (oldnum & (((1 << (self.bits // 2)) - 1) << (self.bits // 2)))

        if dest > Program.cmp: # some registers are read only
            self.regs[dest] = newnum

    def sub(self, inst):
        reg1 = Program.extract(inst, self.bits, 4, 8, False)
        reg2 = Program.extract(inst, self.bits, 8, 12, False)
        dest = Program.extract(inst, self.bits, 12, 16, False)

        if dest > Program.cmp: # some registers are read only
            self.regs[dest] = self.regs[reg1] - self.regs[reg2]

    def add(self, inst):
        reg1 = Program.extract(inst, self.bits, 4, 8, False)
        reg2 = Program.extract(inst, self.bits, 8, 12, False)
        dest = Program.extract(inst, self.bits, 12, 16, False)

        if dest > Program.cmp: # some registers are read only
            self.regs[dest] = self.regs[reg1] + self.regs[reg2]

    def none(self, inst):
        pass

    def initializeRegisters():
        return [0] * Program.bits

    def extract(number, maxbits, firstbit, lastbit, signed):
        #build the mask
        mask = (1 << (lastbit - firstbit)) - 1
        mask = mask << (maxbits - lastbit)

        #apply the mask
        num = (number & mask) >> (maxbits - lastbit)

        #deal with signedness
        if signed:
            num -= (1 << ((lastbit - firstbit) - 1))

        return num

    def numtostr(num, length, signed):
        temp = num
        if signed:
            temp += 1 << (length - 1)

        if temp < 0:
            temp = 0

        temp = temp & ((1 << length) - 1)

        return bin(temp)[2:].zfill(length)


if __name__ == "__main__":
    testprog = Program([
        '0000011000110011',
        '0000000000010101',
        '0001010001010100',
        '0100010000000001',
        '1000010000110000',
        '1111011111111100'
    ])

    testprog.runProgram(10)
    
    print(testprog.out)
