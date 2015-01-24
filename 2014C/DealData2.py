import numpy as np 
import re
import math
import Queue

def cmpd(a,b):
	return cmp(b.D,a.D)

def cmpc(a,b):
	return cmp(b.C,a.C)

def cmpl(a,b):
	return cmp(a.L,b.L)

def cmpt(a,b):
	return cmp(b.T,a.T)

class Node():
	def __init__(self,name,id,num):
		if (id == None):
			print 'hehehe: ',name
		self.name = name
		self.id = id
		self.num = num
		self.D = 0
		self.C = 0
		self.L = 0
		self.T = 0

	def set_DCL(self,D,C,L):
		self.D = D
		self.C = C
		self.L = L
		self._L = 511.0/L

	def set_topsis(self,topsis):
		self.T = topsis

	def pri(self):
		return 'name: %s\nid: %d\tnum: %d\tD: %d\tC: %f\tL: %f Topsis: %f' % (self.name, self.id, self.num, self.D, self.C, self.L, self.T)



#get the matrix
class DealData():
	def __init__(self,filename):
		self.filename = filename
		self.num_of_point = 0
		#self.mat = np.array([[0 for i in range(self.num_of_point)] for j in range(self.num_of_point)])
		self.ID = dict()
		self.Name = list()
		self.pattern = re.compile(r'\d{4}')
		self.node = list()
		self.edge = list()
		self.degree = list()
		self.degree_distributed = list()
		self.L = list()
		self.C = list()
		self.maxD = 0

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

	def add_id(self,name):
		self.ID[name] = self.num_of_point
		self.Name.append(name)
		self.num_of_point += 1
		return self.ID[name]

	def get_id(self,name):
		if self.ID.get(name) == None:
			return -1
		return self.ID[name]

	def get_name_num(self,name):
		tmp = name.split(':')
		ret = 1
		if len(tmp) == 2:
			ret = int(tmp[1])
		return ret

	def get_num_of_point(self):
		f = open(self.filename)
		lines = f.readlines()
		#print lines
		for line in lines:
			if line == '':
				continue
			#print line
			if self.is_match(line):
				if line.strip() == '':
					continue
				name = self.deal_name(line)
				u = self.add_id(name)
				self.node.append(Node(name,u,self.get_name_num(line)))

		for line in lines:
			if line == '':
				continue
			#print line
			if self.is_match(line):
				name = self.deal_name(line)
				u = self.get_id(name)
			else:
				name = self.deal_name(line)
				v = self.get_id(name)
				if v != -1:
					self.edge.append([u,v])
		print self.num_of_point
		f.close()

	def get_matrix(self):
		print len(self.edge)
		self.mat = [[0 for i in range(self.num_of_point)] for j in range(self.num_of_point)]
		for [u,v] in self.edge:
			self.mat[u][v] = 1
			self.mat[v][u] = 1
			print u,' ',v
		#print self.mat
	
	def get_degree(self):
		self.degree = [0 for i in range(self.num_of_point)]
		for i in range(self.num_of_point):
			self.degree[i] = sum(self.mat[i])

	def get_degree_distributed(self):
		self.degree_dsitributed = [0 for i in range(self.num_of_point)]
		for i in self.degree:
			self.degree_dsitributed[i] += 1

	def get_a_point_Ci(self,p):
		tmp = list()
		#tmp.append(p)
		for i in range(self.num_of_point):
			if self.mat[p][i] == 1:
				tmp.append(i)
		print "node:", p,' ',tmp
		n = len(tmp)
		k = 0
		if n <= 1:
			return 0
		for i in tmp:
			for j in tmp:
				if i < j:
					k += self.mat[i][j]
		return k * 2.0 / (n * (n-1))

	def get_C(self):
		self.C = [0 for i in range(self.num_of_point)]
		for i in range(self.num_of_point):
			self.C[i] = self.get_a_point_Ci(i)
		return sum(self.C) / self.num_of_point

	def get_a_point_Li(self,p):
		vis = [0 for i in range(self.num_of_point)]
		#BFS
		vis[p] = 0;
		q = Queue.Queue()
		q.put(p)
		while not q.empty():
			h = q.get()
			for i in range(self.num_of_point):
				if self.mat[h][i] and i != q and vis[i] == 0:
					vis[i] = vis[h]+1
					q.put(i)
		if self.maxD < max(vis):
			self.maxD = max(vis)
		for i in range(self.num_of_point):
			if vis[i] == 0 and i != p:
				vis[i] = 11
		return sum(vis)

	def get_L(self):
		self.L = [0 for i in range(self.num_of_point)]
		for i in range(self.num_of_point):
			self.L[i] = self.get_a_point_Li(i)
		return sum(self.L) / (2.0 * self.num_of_point * (self.num_of_point-1))

	def update_node_list(self):
		for i in range(self.num_of_point):
			self.node[i].set_DCL(self.degree[i], self.C[i], self.L[i])

	def output_node_list(self,filename):
		f = open(filename,'w')
		f.write('num_of_point: %d D:%d\n' % (self.num_of_point,self.maxD))
		for i in self.node:
			#print i.name,' ',i.id,' ',i.num,' ',i.D,' ',i.C,' ',i.L
			f.write(i.pri())
			f.write('\n')
		f.close()
		#sort by d
		self.node.sort(cmpd)
		f = open('d'+filename,'w')
		f.write('num_of_point: %d D:%d\n' % (self.num_of_point,self.maxD))
		for i in self.node:
			#print i.name,' ',i.id,' ',i.num,' ',i.D,' ',i.C,' ',i.L
			f.write(i.pri())
			f.write('\n')
		f.close()
		
		#sort by c
		self.node.sort(cmpc)
		f = open('c'+filename,'w')
		f.write('num_of_point: %d D:%d\n' % (self.num_of_point,self.maxD))
		for i in self.node:
			#print i.name,' ',i.id,' ',i.num,' ',i.D,' ',i.C,' ',i.L
			f.write(i.pri())
			f.write('\n')
		f.close()

		#sort by l
		self.node.sort(cmpl)
		f = open('l'+filename,'w')
		f.write('num_of_point: %d D:%d\n' % (self.num_of_point,self.maxD))
		for i in self.node:
			#print i.name,' ',i.id,' ',i.num,' ',i.D,' ',i.C,' ',i.L
			f.write(i.pri())
			f.write('\n')
		f.close()
		#sort by t
		self.node.sort(cmpt)
		f = open('t'+filename,'w')
		f.write('num_of_point: %d D:%d\n' % (self.num_of_point,self.maxD))
		for i in self.node:
		#	print i.name,' ',i.id,' ',i.num,' ',i.D,' ',i.C,' ',i.L
			f.write(i.pri())
			f.write('\n')
		f.close()

	def cal_dis(self,a,b):
		for i in range(3):
			ret = (a[i]-b[i])**2
		ret = math.sqrt(ret)
		return ret

	def cal_topsis(self):
		topmat = np.array([[0 for i in range(3)] for j in range(self.num_of_point)], dtype = np.float)
		for i in range(self.num_of_point):
			topmat[i][0] = self.node[i].D
			topmat[i][1] = self.node[i].C
			topmat[i][2] = self.node[i]._L
			#topmat[i][3] = self.node[i].num
		s = sum(topmat)
		print s
		for i in range(self.num_of_point):
			for j in range(3):
				topmat[i][j] = topmat[i][j] / s[j];

		good = np.array([0,0,0], dtype = np.float)
		bad = np.array([1,1,1], dtype = np.float)
		for i in range(self.num_of_point):
			for j in range(3):
				if topmat[i][j] > good[j]:
					good[j] = topmat[i][j]
				if topmat[i][j] < bad[j]:
					bad[j] = topmat[i][j]
				#bad[j] = min(bad[j],topmat[i][j])
		print topmat
		print good
		print bad
		Lgood = [0 for i in range(self.num_of_point)]
		Lbad = [0 for i in range(self.num_of_point)]
		for i in range(self.num_of_point):
			Lgood[i] = self.cal_dis(good,topmat[i])
			Lbad[i] = self.cal_dis(bad,topmat[i])
		for i in range(self.num_of_point):
			self.node[i].T = Lbad[i] / (Lbad[i] + Lgood[i])





A = DealData('Data.in')
A.get_num_of_point()
A.get_matrix()
#print A.mat
A.get_degree()
A.get_degree_distributed()
A.get_C()
A.get_L()
A.update_node_list()
A.cal_topsis()
A.output_node_list('Data.out')


