import tensorflow as tf
import numpy as np
import random 



class CodeGenRNN:
	def __init__(self, session, in_size, out_size, num_layers, lstm_size, learning_rate=0.003, name="rnn"):
		self.session = session
		self.in_size = in_size
		self.out_size = out_size
		self.num_layers = num_layers
		self.lstm_size = lstm_size
		self.learning_rate = learning_rate
		self.name = name


		self.lstm_last_state = np.zeros((self.num_layers*2*self.lstm_size,))

		self.x_input = tf.placeholder(tf.float32, 
				shape=(None, None, self.in_size))
		self.y_input = tf.placeholder(tf.float32,
				shape=(None, None, self.in_size))

		self.lstm_init_value = tf.placeholder(tf.float32, 
				shape=(None, self.num_layers*2*self.lstm_size), 
				name='lstm_init_value')

		self.lstm_cells = [tf.contrib.rnn.BasicLSTMCell(
			self.lstm_size,
			forget_bias=1.0, 
			state_is_tuple=False,
			) for i in range(self.num_layers)]

		self.lstm = tf.contrib.rnn.MultiRNNCell(
				self.lstm_cells, state_is_tuple=False)

		outputs, self.lstm_new_state = tf.nn.dynamic_rnn(
				self.lstm, self.x_input, 
				initial_state=self.lstm_init_value,
				dtype=tf.float32)


		self.rnn_out_W = tf.Variable(tf.random_normal(
				(self.lstm_size, self.out_size),
				stddev=0.01))

		self.rnn_out_B = tf.Variable(tf.random_normal(
				(self.out_size,),
				stddev=0.01))

		outputs_reshaped = tf.reshape(outputs, [-1, self.lstm_size])
		network_output = (
				tf.matmul(outputs_reshaped, self.rnn_out_W) + self.rnn_out_B)

		batch_time_shape = tf.shape(outputs)
		self.final_outputs = tf.reshape( 
				tf.nn.softmax( network_output), 
				(batch_time_shape[0], batch_time_shape[1], 
				self.out_size) )


		y_batch_long = tf.reshape(self.y_input, [-1, self.out_size])

		self.cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(
			logits=network_output, labels=y_batch_long))

		self.train_op = tf.train.RMSPropOptimizer(
			self.learning_rate, 0.9).minimize(self.cost)



	def run_step(self, x, init_zero_state=True):
		if init_zero_state:
			init_value = np.zeros((self.num_layers*2*self.lstm_size,))
		else:
			init_value = self.lstm_last_state
		out, next_lstm_state = self.session.run([
			self.final_outputs, self.lstm_new_state],
			feed_dict={self.x_input:[x], self.lstm_init_value:[init_value]})
		self.lstm_last_state = next_lstm_state[0]
		return out[0][0]


	def train_batch(self, X, y):
		init_value = np.zeros((X.shape[0], self.num_layers*2*self.lstm_size))
		cost, _ = self.session.run([self.cost, self.train_op], 
				feed_dict={
					self.x_input:X, 
					self.y_input:y, 
					self.lstm_init_value:init_value})
		return cost


