import re
import numpy as np

class DealData():
	def __init__(self):
		self.maxn = 10000
		self.tot = 0;
		self.ID = dict()
		self.Name = [' ' for i in range(self.maxn)]
		self.mat = [[0 for i in range(self.maxn)] for j in range(self.maxn)]
		self.pattern = re.compile(r'\d{4}')
		self.degree = [0 for i in range(self.maxn)]
		self.mat2 = np.array()
		self.pos = list()
		self.num_of_ones

	def get_id(self,name):
		if not self.ID.get(name):
		#	print name
			self.ID[name] = self.tot
			self.Name[self.tot] = name
			self.tot += 1
	#		print 'hehehehe'
		return self.ID[name]

	def get_name(self,id):
		return self.Name[id]

	def is_match(self,name):
		if self.pattern.search(name):
			return True
		return False

	def deal_name(self,name):
		ret = name
		match = self.pattern.search(name)
		if match:
			ret = ret[0:match.start()]
		ret = ret.strip()
		ret = ret.upper()
		if (ret == ''):
			print "wrong", name
		return ret

	def get_num(self,filename):
		f = open(filename)
		lines = f.readlines()
		for line in lines:
			if line.strip() == '':
				continue;
			line = self.deal_name(line)
			self.get_id(line)
		Ks = list(self.ID.keys())
		Ks.sort()
		for k in Ks:
			print k,' ',self.ID[k]
		print self.tot
	def get_matrix(self,filename):
		f = open(filename)
		lines = f.readlines()

		for line in lines:
			if line.strip() == '':
				continue
			if self.is_match(line):
				line = self.deal_name(line)
				u = self.get_id(line)
			else:
				line = self.deal_name(line)
				v = self.get_id(line)
				self.mat[u][v] = 1
				self.mat[v][u] = 1	

	def pri(self):
		#print sorted(self.ID.items(), key=lambda d: d[0])
		for k in self.ID:
			print 'name:',k,' id:',self.ID[k]
		Ks = list(self.ID.keys())
		Ks.sort()
		for k in Ks:
			print k,' ',self.ID[k]

	def mycmp(self,a,b):
		return cmp(b,a)

	def get_final(self):
		for i in range(9787):
			self.degree[i] = sum(self.mat[i]) * 10000 + i
		self.num_of_ones = 0
		self.degree.sort(self.mycmp)
		for i in self.degree:
			if i / 10000 != 1:
				print self.get_name(i%10000),' degree:',i / 10000
			if i / 10000 > 1:
				self.num_of_ones += 1
				self.pos.append(i%10000)
		print 'num of one:',self.num_of_ones
		self.pos.sort()
		print 'size:', len(self.mat)
		self.mat = np.array(self.mat)
		self.mat2 = self.mat[pos, pos]




a = DealData()
a.get_num('Data.in')
a.get_matrix('Data.in')
a.get_final()
#a.pri()
