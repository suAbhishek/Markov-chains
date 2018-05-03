import re
import pickle
import random

class MarkovChain:
	def __init__(self):
		self.tree = dict()
		self.newtree = dict()

	def train(self,txt, factor = 1.0):
		#extracting words from the text
		words = filter(lambda str: len(str)>0, re.split(r'[\s]',txt))

		#converting each letter of word in words lower case
		words = [w.lower() for w in words]

		for a,b in [(words[i],words[i+1]) for i in range(len(words)-1)]:
			if a not in  self.tree:
				self.tree[a] = dict()

			if b not in self.tree[a]:
				self.tree[a][b] = factor
			else:
				self.tree[a][b] = self.tree[a][b] + self.tree[a][b]*factor
	   # self.generatestr(self.tree)


	def trainwithfile(self,file_name):
		try:
			with open(file_name,'r') as file:
				self.train(file.read())
		except FileNotFoundError:
			print("Not able to open the file")

	'''Save the tree into a file'''

	def savetraining(self,file):
		with open(file,'wb') as f:
			pickle.dump(self.tree,f)

	'''Load the tree  from a file'''
	def loadfile(self,file):
		with open(file,'rb') as f:
			self.tree = pickle.load(f)


	def randomize(self):
		for w, k in self.tree.items():
			size = len(k)
			for ks in k:
				self.tree[w][ks] = (random.random() * self.tree[w][ks]) / size

	def makenew(self):
		for k,v in self.tree.items():
#			print(k, " " , v)
			if isinstance(v,dict):
				self.newtree[k] = [(v1,v2) for v2,v1 in v.items()]
				self.newtree[k].sort()
				self.newtree[k] = [(v2,v1) for v2,v1 in v.items()]


		#rand = lambda x: random.random() * x
	def generatestr(self, start = None):

		if len(self.tree) == 0:
			return

		if start is not None:
			word = start
		else:
			word = random.choice([key for key in self.tree])

		#random starting word -- word
		i =1

		self.randomize()
		self.makenew()

		sentence = word
		while i<50:
			if word in self.newtree.keys():
				if ( len(self.newtree[word]) > 1):

					word,val = self.newtree[word][1]
					sentence = sentence + " " + word
					i = i + 1
				else:
					word = random.choice([key for key in self.newtree])
				self.randomize()
				self.makenew()

		return sentence


	# needs to be modified
	def generateformatted(self, exceed_margin = True,word_wrap = 80, start_with = None, max_len = 0, cap_chars = '.?"', newline_chars = '.?!', rand = lambda x : random.random() * x):

		#word wrap counter
		ww = 0

		lc = cap_chars[0] if len(cap_chars) > 0 else ''

		for w in self.generatestr(start=None):

			wstr = w.capitalize() if lc in cap_chars else w[0] + w[1:] if w[0] in cap_chars else w
			wstr += '' if w[-1] not in newline_chars else '\n'
			print(wstr, end=" ")


		if word_wrap > 0:
			ww += len(wstr)
			if wstr[-1] == '\n':
				ww = 0

			if ww >= word_wrap:

				if exceed_margin:
					wstr += '\n'
					ww = 0

				else:
					i = len(wstr) - ww + word_wrap
					wstr = wstr[:1] + '\n' + wstr[1:]
					ww -= word_wrap

		return wstr



