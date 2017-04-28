import sys
import os
from glob import glob
import numpy as np
from network import CodeGenRNN
import tensorflow as tf
import random
from sklearn.externals import joblib
from sklearn.pipeline import Pipeline
from processing_pipeline import OneHotEncoder, RemoveSpace, RemoveComments
import network_config as config
import pandas as pd

def batch(X, time_steps=100, batch_size=128, batch_count=20000):
	ids = range(data.shape[0]-time_steps-1)
	X_batch = np.zeros((batch_size, time_steps, X.shape[1]))
	y_batch = np.zeros((batch_size, time_steps, X.shape[1]))
	for count in range(batch_count):
		batch_ids = random.sample(ids, batch_size)
		for i, data_id in enumerate(batch_ids):
			X_batch[i, :, :] = data[data_id:data_id+time_steps]
			y_batch[i, :, :] = data[data_id+1:data_id+1+time_steps]
		yield X_batch, y_batch


data_dir = os.environ['RAND_LOGIC_DATA']
file_extensions = set(['c', 'C'])
files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(data_dir) for f in filenames if f.split('.')[-1] in file_extensions]
print("File count = {}".format(len(files)))
data = ""
for file in files:
	with open(file, 'r') as f:
		for line in f:
			line = line.strip()
			if line == '':
				continue
			data += line

pipeline = Pipeline([
		("remove_comments", RemoveComments()),
		("remove_space", RemoveSpace()),
		("one_hot_encode", OneHotEncoder()),
		])

data = pipeline.fit_transform(data)

joblib.dump(pipeline, 'saved/pipeline.pkl')

in_size = out_size = data.shape[1]

with tf.Session() as sess: 

	net = CodeGenRNN(
	session=sess,
	in_size=in_size, 
	out_size=out_size, 
	num_layers=config.num_layers, 
	lstm_size=config.lstm_size)

	sess.run(tf.global_variables_initializer())
	saver = tf.train.Saver(tf.global_variables())

	for step, [X_batch, y_batch] in enumerate(batch(
			data, config.time_steps, config.batch_size, 
			batch_count=config.num_train_batches)):
		if step % 1000 == 0:
			saver.save(sess, "saved/model.ckpt")
		cost = net.train_batch(X_batch, y_batch)
		print('Step {} Cost = {}'.format(step, cost))

	saver.save(sess, "saved/model.ckpt")
















