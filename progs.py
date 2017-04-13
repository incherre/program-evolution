# This file contains programs that have been sucessfully evolved by the system

from vmengine import Program

# The first program to be completed, this one says hello world.
helloworld = [ 
    '0100011001000101',
    '0100011100111001',
    '0100111101010101',
    '0100000001010101',
    '0100001001100001',
    '0000001010011000',
    '0100100011010101',
    '0100111010000001',
    '0100010101100001',
    '0100110001101101',
    '0100011001010101',
    '0100101100110101']
testprog = Program(helloworld)
testprog.runProgram(1)
print(testprog.out)

# This one loops and prints many d's
# This program showed up in the first 3 generations
loop1 = ['1011111111110101',
         '0100101100110101',
         '1001110001100111',
         '1101001001000000',
         '1011100000011010']
testprog = Program(loop1)
testprog.runProgram(0.1)
print(testprog.out)
