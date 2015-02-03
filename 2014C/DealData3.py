import math
import numpy as np
import Queue
import re
import matplotlib.pyplot as plt
import networkx as nx

def cmpd(a,b):
	return cmp(b.D,a.D)

def cmpc(a,b):
	return cmp(b.C,a.C)

def cmpl(a,b):
	return cmp(a.L,b.L)

def cmpt(a,b):
	return cmp(b.T,a.T)

def cmpt2(a,b):
	return cmp(b.T2,a.T2)

class Node():
	def __init__(self,name,id,num,time):
		if (id == None):
			print 'hehehe: ',name
		self.name = name
		self.id = id
		self.num = num
		self.time = time
		self.D = 0
		self.C = 0
		self.L = 0
		self.T = 0
		self.num_of_coop = 0
		self.infl = 0

	def set_DCL(self,D,C,L):
		self.D = D
		self.C = C
		self.L = L
		self._L = 70.0/L

	def set_num_of_coop(self,num_of_coop):
		self.num_of_coop = num_of_coop

	def set_infl(self,infl):
		self.infl = infl

	def set_topsis(self,topsis):
		self.T = topsis

	def set_topsis2(self,topsis2):
		self.T2 = topsis2

	def pri(self):
		return 'name: %s\nid: %d\tnum: %d\tD: %d\tC: %f\tL: %f\tcoop:  %d\tyears: %d\tinfl: %f\tTopsis: %f Topsis2: %f' % \
			(self.name, self.id, self.num, self.D, self.C, self.L, self.num_of_coop, self.time, self.infl, self.T, self.T2)



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
		self.CC = 0
		self.LL = 0

	def is_match(self,name):
		if name[0] == '-':
			return True
		return False

	def deal_name(self,name):
		str = name.split(':')
		ret = str[0][1:]		
		ret = ret.upper()
		if (ret == ''):
			print "wrong", name
		return ret

	def get_time(self,name):
		return self.num_of_point

	def add_id(self,name):
		self.ID[name] = self.num_of_point
		self.Name.append(name)
		self.num_of_point += 1
		return self.ID[name]

	def get_id(self,name):
		if name == 'WILLIAM':
			return -2
		if self.ID.get(name) == None:
			return -1
		return self.ID[name]

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
				u = self.get_id(name)
				if u == -1:
					u = self.add_id(name)
					self.node.append(Node(name,u,0,self.get_time(line)))

		num_of_coop = [0 for i in range(self.num_of_point)]
		u = -1
		for line in lines:
			if line == '':
				continue
			#print line
			if self.is_match(line):
				name = self.deal_name(line)
				v = self.get_id(name)
				if u == -2 and v >= 0:
					self.node[v].num += 1
				if u >= 0 and v >= 0:
					self.edge.append([u,v])
					num_of_coop[v] += 1
				u = v
		for i in range(self.num_of_point):
			self.node[i].set_num_of_coop(num_of_coop[i])
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

	def draw_degree(self):
		plt.figure(figsize=(8,4))
		plt.plot(range(20),self.degree_dsitributed[0:20])

		plt.xlabel('Degree')
		plt.ylabel('Number')

		plt.show()


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
		self.CC = sum(self.C) / self.num_of_point
		return self.CC

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
				vis[i] = 6
		return sum(vis)

	def get_L(self):
		self.L = [0 for i in range(self.num_of_point)]
		for i in range(self.num_of_point):
			self.L[i] = self.get_a_point_Li(i)
		self.LL = sum(self.L) / (self.num_of_point * (self.num_of_point-1))
		return self.LL

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
		#sort by t2
		self.node.sort(cmpt2)
		f = open('t2'+filename,'w')
		f.write('num_of_point: %d D:%d CC: %f LL: %f\n' % (self.num_of_point,self.maxD,self.CC,self.LL))
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

	def cal_dis4(self,a,b):
		for i in range(4):
			ret = (a[i]-b[i])**2
		ret = math.sqrt(ret)
		return ret

	def cal_topsis(self):
		topmat = np.array([[0 for i in range(3)] for j in range(self.num_of_point)], dtype = np.float)
		for i in range(self.num_of_point):
			topmat[i][0] = self.node[i].D
			topmat[i][1] = self.node[i].num
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


	def cal_infl(self):
		for i in range(self.num_of_point):
			tmp = 0
			st = 0.0
			for j in range(self.num_of_point):
				if self.mat[i][j] == 1:
					st += self.node[j].T
					tmp += 1
			if tmp == 0:
				self.node[i].set_infl(0)
			else:
				self.node[i].set_infl(st / tmp)


	def cal_topsis2(self):
		topmat = np.array([[0 for i in range(3)] for j in range(self.num_of_point)], dtype = np.float)
		for i in range(self.num_of_point):
			topmat[i][0] = 100/self.node[i].time
			topmat[i][1] = self.node[i].C
			topmat[i][2] = self.node[i].infl*self.node[i].D
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
			self.node[i].T2 = Lbad[i] / (Lbad[i] + Lgood[i])

	def out_pajek(self):
		g = nx.Graph()
		g.add_nodes_from(range(self.num_of_point))
		g.add_edges_from(self.edge)
		nx.write_pajek(g,'g2.net')





A = DealData('bh.utf8')
A.get_num_of_point()
A.get_matrix()
#print A.mat
A.get_degree()
A.get_degree_distributed()
A.get_C()
A.get_L()
A.update_node_list()
A.cal_topsis()
A.cal_infl()
A.cal_topsis2()
A.output_node_list('_bh_Data4.out')
A.out_pajek()
A.draw_degree()


