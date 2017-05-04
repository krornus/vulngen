import os
import numpy as np
import random
from gen_rand import rand_code
import uuid

def rand():
	return random.choice(['', 'rand\n'])

def start():
	input = rand()
	input += vulnerable()
	input += rand()
	return input

def vulnerable():
	input = datatype()
	input += int_int()
	input += loopsection()
	return input

def datatype():
	return random.choice(['char ', 'int ', 'long '])

def int_int():
	return '{} {}\n'.format(random.randrange(5,100), random.randrange(5,100))

def loopsection():
	input = looptype()
	input += pos()
	input += direction()
	input += section()
	return input

def looptype():
	return random.choice(['while ', 'do '])

def pos():
	return random.choice(['pre ', 'post '])

def direction():
	return random.choice(['inc ', 'dec ', 'ptr '])

def section():
	input = '{\n'
	input += rand()
	input += 'set\n'
	input += rand()
	input += '}\n'
	return input

def remove(file):
	try:
		os.remove(file)
	except:
		pass

def format_poet_code(code, output):
	with open('tmp', 'w') as f:
		f.write('\n'.join(code))
	file = './{}/{}.c'.format(output, uuid.uuid4())
	os.system("pcg proj.pt < tmp > {}".format(file))
	if '' == ''.join(open(file, 'r').readlines()).strip():
		remove(file)
	remove('tmp')


def stripmain(code):
	return code[2:-3]

def splitvarandlogic(code):
	variables = []
	logic = []
	for line in code:
		s_line = line.strip()
		if (s_line.startswith('int') or
			s_line.startswith('float') or
			s_line.startswith('char')):
			variables.append(line)
		else:
			logic.append(line)

	return variables, logic

	
def create_code():
	rand_code_gen = rand_code()
	for i in range(100):
		with open('p_input', 'w') as f:
			f.write(start())
		os.system('cd ../; pcg proj.pt < {} > ./rand_logic/code.c'.format('./rand_logic/p_input'))
		remove('./p_input')
		code = []

		r_code = next(rand_code_gen)
		variables, logic = splitvarandlogic(stripmain(r_code))
		with open('code.c', 'r') as f:
			for line in f:
				if line.strip() == 'variables':
					code.extend(variables)
				elif line.strip() == 'random':
					code.extend(logic)
				else:
					code.append(line)

		remove('code.c')
		format_poet_code(code, '/final_code')


create_code()