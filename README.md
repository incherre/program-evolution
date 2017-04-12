# Evolving Code
This project is a small experiment to explore the feasibility of evolving assembly.

I have specified a simple assembly language and implemented a barebones VM to run it. The VM is designed to be as forgiving as possible of invalid input. Any completely invalid input is considered to be a NOP instruction.

There is a second part that generates random programs, runs them using the VM, and scores them with a fitness function. The best programs continue on to future rounds and are copied (with mutations) to take the place of the worst programs, which are removed.
