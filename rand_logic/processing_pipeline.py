from sklearn.base import BaseEstimator, TransformerMixin
import re
import numpy as np
import pickle

class OneHotEncoder(BaseEstimator, TransformerMixin):
	def __init__(self):
		pass

	def fit(self, X, y=None):
		self.vocab = {}
		for c in list(set(X)):
			self.vocab[c] = len(self.vocab)
		with open('saved/vocab.dict', 'wb') as f:
			pickle.dump(self.vocab, f)
		return self


	def fit_transform(self, X, y=None, **fit_params):
		self.fit(X, y, **fit_params)
		return self.transform(X)

	def transform(self, X):
		data = np.zeros((len(X), len(self.vocab)))
		for i, c in enumerate(X):
			data[i][self.vocab[c]] = 1.0
		return data

class RemoveComments(BaseEstimator, TransformerMixin):
	def __init__(self):
		pass

	def fit(self, X, y=None):
		return self

	def fit_transform(self, X, y=None, **fit_params):
		self.fit(X, y, **fit_params)
		return self.transform(X)

	def transform(self, X):
		return re.sub(r"(/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/)|(//.*)", '', X)

