"""
---------------------------------
	Aman Ali
	CS9163 - Application Security
	Fall 2013
	Turing Complete Sandbox
---------------------------------

	Description: Runs instructions as needed without crashing
"""

'''
-Calculation
	{add,sub,mul,div,nand}
-Control
	{jeq,jne,jl,jg,jmp}
-Memory
	{load} --basically assignment/copy operator
'''

import sys

REG_MAX = 25 		#Max number of registers allowed
MAX_CODE_SIZE = 50	#Limit on code lines
MAX_LINE_SIZE = 30	#Limit on size of each line of code
#List of commands - name & number of parameters
COMMANDS = {'add': 3, 'sub': 3, 'mul' :3, 'div':3, 
			'jeq': 3, 'jne': 3, 'jl': 3, 'jg': 3,
			'jmp': 1, 'load': 2, 'print': 1, 'nand': 3}
#Dict to hold registers - name & value
REGS = {}

def create_vars(reg_num):
	'''Initializes valid registers'''
	count = ord('a')
	for i in range(reg_num):
		REGS[chr(count)] = 0	#initialize registers to 0
		count+=1

def compare(a,b,command):
	'''Returns comparison based on command'''
	return {
	'jeq': a == b,
	'jne': a != b,
	'jl': a < b,
	'jg': a > b
	}.get(command, None)

def branch(reg_1,reg_2,offset,command,PC):
	'''Returns the result of the comparison command on inputs 1 & 2'''
	#Determines if jumping or not
	branch = False
	#Check that both inputs are registers
	if reg_1 in REGS and reg_2 in REGS:
		if compare(REGS[elements[1]],REGS[elements[2]]):
			try:
				offset = int(elements[3])
			except ValueError:
				sys.exit('Line '+str(PC+1)+' has invalid jump offset')
			#Check constraints
			if offset != 0 and PC+offset < len(data) and PC+offset > 0:
				PC += offset
				return True
			#Else invalid offset
			sys.exit('Line '+str(PC+1)+' has invalid jump offset')
	else:
		sys.exit('Line '+str(PC)+' has unknown register')

def calculate(input_1,input_2,command,PC):
	'''Returns the result of the calculation command on inputs 1 & 2'''
	#Evaluate input_1
	if input_1 in REGS:	# operand 1 is a register
		op_1 = REGS[input_1]
	else:
		#operand 1 is an int
		try:
			op_1 = int(input_1)
		except ValueError:
			sys.exit('Line '+str(PC+1)+' has an invalid operand')

	#Evaluate input_2
	if input_2 in REGS:	# operand 2 is a register
		op_2 = REGS[input_2]
	else:
		#operand 2 is an int
		try:
			op_2 = int(input_2)
		except ValueError:
			sys.exit('Line '+str(PC+1)+' has an invalid operand')

	if command == 'add':
		return op_1 + op_2
	elif command == 'sub':
		return op_1 - op_2
	elif command == 'mul':
		return op_1 * op_2
	elif command == 'div':
		if op_2 == 0:
			sys.exit('Line '+str(PC+1)+' tried to divide by zero')
		else:
			return op_1/op_2
	elif command == 'nand':
		return ~(a & b)
	else:
		sys.exit('Line '+str(PC+1)+' has invalid command')
	
	return

def process(data):
	'''Runs program and prints output'''
	PC = 0		#Program Counter
	if len(data[PC]) > MAX_LINE_SIZE:
		sys.exit('Line '+str(PC+1)+' too long')
	if data[PC] != 'begin\n':
		sys.exit('Incorrect Header, program must start with begin statement ')

	PC += 1

	while True:
		#print 'PC-',PC+1
		#first check data[PC] length
		try:
			if len(data[PC]) > MAX_LINE_SIZE:
				sys.exit('Line '+str(PC+1)+' too long')
		except:
			sys.exit('Line '+str(PC+1)+' invalid')

		#check if EOF
		if data[PC].strip() == 'end':
			break

		#Get line elements
		elements = data[PC].strip().split()

		#print elements

		#exit if line empty or just one command
		#Smallest command has 2 elements
		if len(elements) < 2:
			sys.exit('Line '+str(PC+1)+' malformed')


		#exit if invalid command
		if elements[0] not in COMMANDS:
			sys.exit('Line '+str(PC+1)+' has invalid command')

		#match position in commands to params
		if len(elements)-1 != COMMANDS[elements[0]]:
			sys.exit('Line '+str(PC+1)+' has too few/many parameters')

		#process calculation commands
		if elements[0] in ['add','sub','mul','div','nand']:
			if elements[1] in REGS:		#output register
				REGS[elements[1]] = calculate(elements[2],elements[3],elements[0],PC)
			else:
				sys.exit('Line '+str(PC+1)+' has unknown register')

		elif elements[0] in ['jeq','jne','jg','jl']:
			#Check that both inputs are registers
			if elements[1] in REGS and elements[2] in REGS:
				if REGS[elements[1]] == REGS[elements[2]]:
					try:
						offset = int(elements[3])
					except ValueError:
						sys.exit('Line '+str(PC+1)+' has invalid jump offset')
					#Check constraints
					if offset != 0 and PC+offset < len(data) and PC+offset > 0:
						PC += offset
						continue
					sys.exit('Line '+str(PC+1)+' has invalid jump offset')
			else:
				sys.exit('Line '+str(PC)+' has unknown register')

		elif elements[0] == 'jmp':
			try:
				offset = int(elements[1])
			except ValueError:
				sys.exit('Line '+str(PC+1)+' has invalid jump offset')
			if offset != 0 and PC+offset < len(data) and PC+offset > 0:
				PC += offset
				continue
			else:
				sys.exit('Line '+str(PC+1)+' has invalid jump offset')

		elif elements[0] == 'load':
			#print elements[1], REGS
			if elements[1] in REGS:
				if elements[2] in REGS:
					value = REGS[elements[2]]
				else:
					try:
						value = int(elements[2])
					except ValueError:
						sys.exit('Line '+str(PC+1)+' has invalid value')

				#if accepted load value into register
				REGS[elements[1]] = value
			else:
				sys.exit('Line '+str(PC+1)+' has unknown register')

		elif elements[0] == 'print':
			if elements[1] in REGS:
				#print register value
				print REGS[elements[1]]
			else:
				sys.exit('Line '+str(PC+1)+' has unknown register')

		PC+=1

def main(argc,argv):
	filename = argv[1]
	
	#exit if reg_num passed in isn't an integer
	try:
		reg_num = int(argv[2])
		#Take care of unusual formats
		if type(reg_num) != int:
			sys.exit('Invalid number entered, enter int for register number')
	except ValueError:
		sys.exit('Enter int for register number ')

	#exit if reg_num is too big or negative
	if reg_num > REG_MAX or reg_num <= 0:
		sys.exit('Too many/few registers, REG_MAX = 25')

	#Open file, making sure it exists
	try:	
		fp = open(filename,'r')
	except IOError:
		sys.exit('Input file missing')

	data = fp.readlines()
	fp.close()

	#Check that code is within size limit
	if len(data) > MAX_CODE_SIZE:
		sys.exit('Input code too big')

	create_vars(reg_num)

	process(data)


if __name__ == '__main__':
	if len(sys.argv) != 3:
		sys.exit('Too few/many arguments. Usage: run.py <input.txt> reg_num')
	main(len(sys.argv),sys.argv)