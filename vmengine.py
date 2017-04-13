import time
import math
import string

class Program:
    'A class representing a particular program to be run on the VM'
    
    bits = 16
    PC = 1
    cmp = 2
    
    def __init__(self, code):
        self.code = code
 
    def runProgram(self, timelimit):
        self.regs = Program.initializeRegisters()
        self.out = ''
        startTime = time.time()

        while (timelimit >= (time.time() - startTime) and self.regs[Program.PC] < len(self.code)):
            self.runInstruction(self.code[self.regs[Program.PC]])
            self.regs[Program.PC] += 1

        self.time = time.time() - startTime

    def runInstruction(self, inst):
        ops = {
            '0000': self.loadb,
            '0001': self.add,
            '0010': self.loadt,
            '0011': self.sub,
            '0100': self.prin,
            '0101': self.none,
            '0110': self.none,
            '0111': self.none,
            '1000': self.lt,
            '1001': self.gt,
            '1010': self.none,
            '1011': self.none,
            '1100': self.no,
            '1101': self.jump,
            '1110': self.eq,
            '1111': self.branch
        }
        opcode = inst[:4]
        ops[opcode](inst)

    def prin(self, inst):
        reg = Program.strtonum(inst[4:8], False)
        offset = Program.strtonum(inst[8:14], False)
        option = Program.strtonum(inst[14:16], False)
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
        reg1 = Program.strtonum(inst[4:8], False)
        reg2 = Program.strtonum(inst[8:12], False)
        if self.regs[reg1] > self.regs[reg2]:
            self.regs[Program.cmp] = 1
        else:
            self.regs[Program.cmp] = 0

    def lt(self, inst):
        reg1 = Program.strtonum(inst[4:8], False)
        reg2 = Program.strtonum(inst[8:12], False)
        if self.regs[reg1] < self.regs[reg2]:
            self.regs[Program.cmp] = 1
        else:
            self.regs[Program.cmp] = 0

    def eq(self, inst):
        reg1 = Program.strtonum(inst[4:8], False)
        reg2 = Program.strtonum(inst[8:12], False)
        if self.regs[reg1] == self.regs[reg2]:
            self.regs[Program.cmp] = 1
        else:
            self.regs[Program.cmp] = 0

    def branch(self, inst):
        offset = Program.strtonum(inst[4:16], True)
        if self.regs[Program.cmp] == 1:
            self.regs[Program.PC] += offset
            if self.regs[Program.PC] < 0:
                self.regs[Program.PC] = 0

    def jump(self, inst):
        jreg = Program.strtonum(inst[12:16], False)
        offset = Program.strtonum(inst[4:12], True)
        jumplocation = self.regs[jreg] + offset
        if jumplocation < 0:
            jumplocation = 0
        self.regs[Program.PC] = jumplocation

    def loadt(self, inst):
        dest = Program.strtonum(inst[12:16], False)
        top = inst[4:12]
        oldstring = Program.numtostr(self.regs[dest], Program.bits, False)
        newstring = top + oldstring[8:]

        if dest > Program.cmp: # some registers are read only
            self.regs[dest] = Program.strtonum(newstring, False)

    def loadb(self, inst):
        dest = Program.strtonum(inst[12:16], False)
        bottom = inst[4:12]
        oldstring = Program.numtostr(self.regs[dest], Program.bits, False)
        newstring = oldstring[:8] + bottom

        if dest > Program.cmp: # some registers are read only
            self.regs[dest] = Program.strtonum(newstring, False)

    def sub(self, inst):
        reg1 = Program.strtonum(inst[4:8], False)
        reg2 = Program.strtonum(inst[8:12], False)
        dest = Program.strtonum(inst[12:16], False)

        if dest > Program.cmp: # some registers are read only
            self.regs[dest] = self.regs[reg1] - self.regs[reg2]

    def add(self, inst):
        reg1 = Program.strtonum(inst[4:8], False)
        reg2 = Program.strtonum(inst[8:12], False)
        dest = Program.strtonum(inst[12:16], False)

        if dest > Program.cmp: # some registers are read only
            self.regs[dest] = self.regs[reg1] + self.regs[reg2]

    def none(self, inst):
        pass

    def initializeRegisters():
        return [0] * Program.bits

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
