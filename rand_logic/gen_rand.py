import tensorflow as tf
from sklearn.externals import joblib
from processing_pipeline import RemoveComments
from network import CodeGenRNN
import pickle
import network_config as config
import numpy as np

pipline = joblib.load('saved/pipeline.pkl')
with open('saved/vocab.dict', 'rb') as f:
	vocab = pickle.load(f)
reverse_vocab = {v: k for k, v in vocab.items()}

test="int"

with tf.Session() as sess: 

	net = CodeGenRNN(
	session=sess,
	in_size=len(vocab), 
	out_size=len(vocab), 
	num_layers=config.num_layers, 
	lstm_size=config.lstm_size)

	sess.run(tf.global_variables_initializer())
	saver = tf.train.Saver(tf.global_variables())
	saver.restore(sess, "saved/model.ckpt")

	data = pipline.transform(test)
	for i in range(data.shape[0]):
		out = net.run_step([data[i]], i==0)

	print('Code:')
	gen_code = test
	for i in range(500):
		element = np.random.choice(range(len(vocab)), p=out)
		element = reverse_vocab[element]
		gen_code += element
		if element == ';':
			gen_code += '\n'
		out = net.run_step(pipline.transform(element))
	print(gen_code)





