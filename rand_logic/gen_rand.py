import tensorflow as tf
from sklearn.externals import joblib
#from processing_pipeline import RemoveComments
from network import CodeGenRNN
import pickle
import network_config as config
import numpy as np
import uuid
import os
import subprocess
import hashlib
import random

hashes = set()

output_dir = './input'
def write_file(code):
	file = os.path.join(output_dir, str(uuid.uuid4()))
	with open(file, 'w') as f:
		f.write(code)
	return file

def remove_file(file):
	try:
		os.remove(file)
	except:
		pass

def replace_numbers(code):
	for i in range(1, 10):
		code = code.replace('num{}'.format(i), str(random.randrange(5, 100)))
		code = code.replace('float{}'.format(i), 
			str(random.random()*random.randrange(5, 100)))
	return code

def verify(code):
	file = write_file(code)
	#Write the file
	file = format_poet_code(file)
	if file == None:
		#Syntax error
		print('Syntax error')
		return 
	if check_file(file) == False:
		#Dup file
		print('DUP')
		remove_file(file)
		return

	#Check 15 diffrent number combinations
	for i in range(15):
		num_code = replace_numbers(str(code))	
		if compile_and_run_check_clean(num_code) == False:
			#Remove file and exit
			return None
	code =  open(file, 'r').readlines()
	remove_file(file)
	return replace_numbers(''.join(code)).split('\n')

def verify_and_write(code):
	file = write_file(code)
	#Write the file
	file = format_poet_code(file)
	if file == None:
		#Syntax error
		print('Syntax error')
		return 
	if check_file(file) == False:
		#Dup file
		print('DUP')
		remove_file(file)
		return

	#Check 15 diffrent number combinations
	for i in range(15):
		num_code = replace_numbers(str(code))	
		if compile_and_run_check_clean(num_code) == False:
			#Remove file and exit
			remove_file(file)
			return



def format_poet_code(file):
	os.system("pcg proj.pt < {} > {} 2> tmp".format(file, file + '.c'))
	remove_file('tmp')
	remove_file(file)
	#Check if poet wrote the file
	if '' == ''.join(open(file+'.c', 'r').readlines()).strip():
		#If error then remove the file
		remove_file(file + '.c')
		return None
	return file + '.c'

def compile_and_run_check_clean(code):
	file = write_file(code)
	check = compile_and_run_check(file)
	remove_file(file)
	return check

	
def compile_and_run_check(file):
	file_dir = '/'.join(file.split('/')[:-1])
	print('GCC START')
	os.system('gcc -x c {} 2> tmp'.format(file))
	print('GCC END')
	if 'warning' in ''.join(open('tmp', 'r').readlines()):
		return False
	remove_file('tmp')
	if os.path.exists(os.path.join('./', 'a.out')):
		check = True
		print('RUN START')
		os.system('unbuffer ./a.out & sleep 1;kill $! 1> tmp1 2> tmp2')
		if 'No such process' not in ''.join(open('tmp2', 'r').readlines()):
			print('Found Terminated')
			check = False
		else:
			print('No T Found')
			os.system('unbuffer ./a.out >tmp1 2> tmp2')
			print('RUN END')
			
			if open('tmp2', 'r').readlines() != []:
				check = False
			elif 'smashing' in ''.join(open('tmp1', 'r').readline()):
				check = False
		remove_file('a.out')
		remove_file('tmp1')
		remove_file('tmp2')
		return check
	return False

def check_file(file):
	file_hash = hash(''.join(open(file, 'r').readlines()).strip())
	if file_hash in hashes:
		return False
	else:
		hashes.add(file_hash)
		return True

def read_all_files():
	for file in [os.path.join('./input', f) for f in os.listdir('./input')]:
		file_hash = hash(''.join(open(file, 'r').readlines()).strip())
		if file_hash in hashes:
			remove_file(file)
		else:
			hashes.add(file_hash)

def restore_network():
	base = ''
	if not os.path.exists('./saved'):
		base = 'rand_logic'

	pipline = joblib.load(os.path.join(base, 'saved/pipeline.pkl'))
	with open(os.path.join(base,'saved/vocab.dict'), 'rb') as f:
		vocab = pickle.load(f)
	reverse_vocab = {v: k for k, v in vocab.items()}

	sess = tf.Session() 

	net = CodeGenRNN(
	session=sess,
	in_size=len(vocab), 
	out_size=len(vocab), 
	num_layers=config.num_layers, 
	lstm_size=config.lstm_size)

	sess.run(tf.global_variables_initializer())
	saver = tf.train.Saver(tf.global_variables())

	saver.restore(sess, os.path.join(base,"saved/model.ckpt"))

	return sess, net, pipline, vocab, reverse_vocab


def create_population():
	sess, net, pipline, vocab, reverse_vocab = restore_network()
	start="#include <stdio.h>"
	read_all_files()
	random_ness = 0.0001

	data = pipline.transform(start)
	for i in range(data.shape[0]):
		out = net.run_step([data[i]], i==0)

	print('Code:')
	gen_code = start + '\n'
	for i in range(1000000):
		prob = (out + abs(np.random.normal(0, random_ness, len(out))))
		prob = prob/sum(prob)
		element = np.random.choice(range(len(vocab)), p=prob)
		element = reverse_vocab[element]
		if element == "#":
			#print(gen_code)
			verify_and_write(gen_code)
			gen_code= ''


		gen_code += element
		if element in [';', '>', '}', '{']:
			gen_code += '\n'
		out = net.run_step(pipline.transform(element), False)


def rand_code():
	sess, net, pipline, vocab, reverse_vocab = restore_network()
	start="#include <stdio.h>"
	random_ness = 0.000001

	data = pipline.transform(start)
	for i in range(data.shape[0]):
		out = net.run_step([data[i]], i==0)

	gen_code = start + '\n'
	for i in range(1000000):
		prob = (out + abs(np.random.normal(0, random_ness, len(out))))
		prob = prob/sum(prob)
		element = np.random.choice(range(len(vocab)), p=prob)
		element = reverse_vocab[element]
		if element == "#":
			code = verify(gen_code)
			if code:
				yield code
			gen_code= ''

		gen_code += element
		if element in [';', '>', '}', '{']:
			gen_code += '\n'
		out = net.run_step(pipline.transform(element), False)





if __name__ == '__main__':
	create_population()

