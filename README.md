App_Sec_Assignment_1
====================

Python Sandbox	- Aman Ali

This sandbox runs using a simplied instruction set.

Usage: run.py <input.txt> reg_num

The program takes in an input text file and prints output to terminal. It also takes in the number of registers required for the program as a command line argument.

Registers are named after characters between from 'a' to 'y'. This limits the sandbox to only 25 registers. Registers can only hold integers.When the register number is declared in the command line, the given number of registers (starting from 'a' onwards) will be set to 0. Usage of any register names outside the given range will cause the program to exit.

The code must start with the command 'begin' on a single line and end similarly with 'end'. All code must all fall between these lines.

    begin
    <code>
    end
    
There are also limits on Code Size (50 lines), Line Size (30 characters)

The instructions available within this sandbox are:

    Calculation Instructions:
    	{add,sub,mul,div,nand}
    	
    Control Instructions:
    	{jeq,jne,jl,jg,jmp}
    	
    Memory Instructions:
    	{load}
	
All calculation instructions take in 3 parameters: an output register and two inputs (numbers or registers).

eg from count.txt:
    sub b b 1

The above line does: b=b-1

All control instructions take in 3 parameters except the jmp instruction which takes only one. The first two parameters are two registers that get compared and an integer offset that gets jumped to. In jmp there is only an integer offset.

Format:

    command a b offset

    jeq = 'jump by offset if a=b'
    jne = 'jump by offset if a!=b'
    jl = 'jump by offset if a < b'
    jg = 'jump by offset if a > b'
    
    jmp = 'jump by offset'

eg from fibo.txt:
    jeq d c 7
    jmp -6
    
The first line jumps 7 instructions forward if the two registers d and c contain the same integer.
The second line simply jumps back 6 instructions.

Memory Instructions take simply 2 parameters: a register and a register or number.

eg:
    load a 0
    load d b
    
First line assigns 0 to register a
Second line assigns value of register b to register d
    
