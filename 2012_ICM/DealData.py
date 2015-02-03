import networkx as nxx
import numpy as npp
import CT
import csv
import math
import matplotlib.pyplot as plt

def cmp_val(a,b):
	return cmp(b.CC,a.CC)

class man():
	def __init__(self,name,ID,AA,BB,CC,c1,c2,c3,gorb):
		self.name = name
		self.ID = ID
		self.AA = AA
		self.BB = BB
		self.CC = CC
		self.gorb = gorb
		self.c1 = c1
		self.c2 = c2
		self.c3 = c3

	def pri(self):
		print '%20s\t%d\t%f\t%f\t%f\t%f\t%f\t%f\t%s' % (self.name,self.ID,self.AA,self.BB,self.CC,self.c1,self.c2,self.c3,self.gorb)
	def pri2(self,d):
		print '%d & %s & %d & %f & %f' % (d,self.name,self.ID,self.CC,self.c3)
	def pri3(self,d):
		print '%d , %s , %d , %f , %f' % (d,self.name,self.ID,self.CC,self.c3)


class DealData():
	def __init__(self):

		self.dv = [[0 for i in range(CT.tpnum)] for j in range(CT.pnum)]
		self.wv = [0.0 for i in range(CT.tpnum)]
		self.g = nxx.DiGraph()

		self.name = ['' for i in range(CT.pnum)]
		self.edge = list()
		self.send = [[0 for i in range(CT.pnum)] for j in range(CT.pnum)]
		self.A = [[0.0 for i in range(CT.pnum)] for j in range(CT.pnum)]
		self.B = [[0.0 for i in range(CT.pnum)] for j in range(CT.pnum)]
		self.C = [[0.0 for i in range(CT.pnum)] for j in range(CT.pnum)]
		self.links = [list() for i in range(CT.pnum)]
		self.sum_edge = 0
		self.sum_node = 0
		self.AA = [0.0 for i in range(CT.pnum)]
		self.BB = [0.0 for i in range(CT.pnum)]
		self.CC = [0.0 for i in range(CT.pnum)]
		self.c1 = [0.0 for i in range(CT.pnum)]
		self.c2 = [0.0 for i in range(CT.pnum)]
		self.c3 = [0.0 for i in range(CT.pnum)]
	def get_data(self):	#

		d = csv.reader(file('Names.csv'))
		for line in d:
			if d.line_num == 1:
				continue
			if line[0] != '':
				self.name[int(line[0])] = line[1]

		d = csv.reader(file('Messages.csv'))
		for line in d:
			if d.line_num == 1:
				continue
			if line[0] != '':
				u = int(line[0])
				v = int(line[1])
				for j in range(2,5):
					if line[j] != '':
						if int(line[j]) > 15:
							continue
						self.edge.append([u,v,int(line[j])-1])

	def cal_wv(self):
		for edge in self.edge:
			print edge
			if edge[0] in CT.bed:
				self.wv[edge[2]] += 1
			if edge[1] in CT.bed:
				self.wv[edge[2]] += 1
		s = sum(self.wv)
		for i in range(len(self.wv)):
			self.wv[i] /= s

	def get_g(self):
		self.g.add_nodes_from(range(CT.pnum))
		for edge in self.edge:
			if edge[2] in CT.bed_top:
				if edge[0] in CT.good or edge[1] in CT.good:
					continue
				self.g.add_edge(edge[0],edge[1])

	def get_dv(self):
		for edge in self.edge:
			print edge
			self.dv[edge[0]][edge[2]] = 1
			self.dv[edge[1]][edge[2]] = 1
		#delete
		#delete the edge (with paige2 top7)
        #delete the edge (with este78 ELLIN68 CHRIS0 top 13)
		#self.dv[2][6] = 0
		#self.dv[78][12] = self.dv[68][12] = self.dv[0][12] = 0

	def cal_sv(self,v1,v2):
#		print '--------------------------------------'
#		print self.wv
#		print v1
#		print v2
		s1 = 0.0
		s2 = 0.0
		for i in range(CT.tpnum):
			if v1[i] and v2[i]:
				s1 += self.wv[i]
			if v1[i] or v2[i]:
				s2 += self.wv[i]
		if s2 == 0:
			return 0
#		print s1,' ',s2,' ',s1/s2
#		print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
		return s1/s2

	def get_send(self):
		for edge in self.edge:
			if edge[2] in CT.bed_top:
				#if edge[0] in CT.good or edge[1] in CT.good:
				#	continue
				#if edge[2] == 6 and (edge[0] == 2 or edge[1] == 2):
				#	continue
				#if edge[2] == 12 and (edge[0] in [0,78,68] or edge[1] in [0,78,68]):
				#	continue
				print '------!@#@!#@!------'
				print edge[0],' ',edge[1]
				self.send[edge[0]][edge[1]] = 1


	def cal_A(self):
		#cal A
		A = [[0.0 for i in range(CT.pnum)] for j in range(CT.pnum)]
		for now in range(CT.pnum):
			for i in range(CT.pnum):
				if i == now:
					A[now][i] = 0
				else:
					if self.send[now][i] == 1:
						A[now][i] += 0.5
					else:
						s1 = 0.0
						s2 = 0.0
						for j in range(CT.pnum):
							if self.send[now][j] and self.send[j][i]:
								s1 += 1
							if self.send[now][j] or self.send[j][i]:
								s2 += 1
						if s2 > 0:
							A[now][i] += 0.5*s1/s2
					if self.send[i][now] == 1:
						A[i][now] += 0.5
					else:
						s1 = 0.0
						s2= 0.0
						for j in range(CT.pnum):
							if self.send[i][j] and self.send[j][now]:
								s1 += 1
							if self.send[i][j] or self.send[j][now]:
								s2 += 1
						if s2 > 0:
							A[now][i] += 0.5*s1/s2
		print A
		self.A = A

	def cal_B(self):
		B = [[0.0 for i in range(CT.pnum)] for j in range(CT.pnum)]
		for i in range(CT.pnum):
			for j in range(CT.pnum):
				B[i][j] = B[j][i] = self.cal_sv(self.dv[i],self.dv[j])
		self.B = B

	def cal_C(self):
		for i in range(CT.pnum):
			for j in range(CT.pnum):
				if i == j:
					self.C[i][j] = 0
				else:
					self.C[i][j] = self.alp*self.A[i][j] + (1-self.alp)*self.B[i][j]

	def cal_avg_A_7(self):
		s = 0
		for i in CT.bed:
			for j in CT.bed:
				s += self.A[i][j]
		s /= 36
		return s
	def cal_avg_B_7(self):
		s = 0
		for i in CT.bed:
			for j in CT.bed:
				s += self.B[i][j]
		s /= 36
		return s
	def cal_alp(self):
		avg_A7 = A.cal_avg_A_7()
		avg_B7 = A.cal_avg_B_7()
		self.alp = avg_B7/(avg_B7+avg_A7)

	def cal_A7(self,now):
		s = 0.0
		for i in CT.bed:
			s += self.A[i][now]
		return s / 7
	def cal_B7(self,now):
		s = 0.0
		for i in CT.bed:
			s += self.B[i][now]
		return s / 7
	def cal_C7(self,now):
		s = 0.0
		for i in CT.bed:
			s += self.C[i][now]
		return s / 7

	def gorb(self,now):
		if now in CT.good:
			return 'good'
		if now in CT.bed:
			return 'bad'
		return 'dont know'

	def get_AB(self):
		for i in range(CT.pnum):
			if i in CT.bed or i in CT.good:
				continue
			else:
				self.AA[i] = self.cal_A7(i)
				self.BB[i] = self.cal_B7(i)

	def cal_dis(self,v1,v2):
		l = len(v1)
		s = 0.0
		for i in range(l):
			s += (v1[i]-v2[i]) ** 2
		return math.sqrt(s)

	def cal_topsis(self,v1,v2):
		l = len(v1)
		#print v1
		#print v2
		v3 = [0.0 for i in range(l)]
		s1 = sum(v1)
		s2 = sum(v2)
		for i in range(l):
			v1[i] /= s1
			v2[i] /= s2
		max1 = min1 = v1[0]
		max2 = min2 = v2[0]
		for i in range(l):
			max1 = max(max1,v1[i])
			max2 = max(max2,v2[i])
			min1 = min(min1,v1[i])
			min2 = min(min2,v2[i])
		#print v1,v2
		#print max1,max2,min1,min2
		for i in range(l):
			D1 = self.cal_dis([max1,max2],[v1[i],v2[i]])
			D2 = self.cal_dis([min1,min2],[v1[i],v2[i]])
			v3[i] = D2/(D1+D2)
		print '~~~~~~~~~~',v3
		return v3
	def get_fri(self):
		for edge in self.edge:
			if not edge[2] in CT.bed_top:
				continue
			if edge[0] in CT.good or edge[1] in CT.good:
				continue
		#	if edge[2] == 6 and (edge[0] == 2 or edge[1] == 2):
		#		continue
			#if edge[2] == 12 and (edge[0] in [0,78,68] or edge[1] in [0,78,68]):
		#		continue
			self.links[edge[0]].append([edge[1],edge[2]])
			self.links[edge[1]].append([edge[0],edge[2]])
			self.sum_edge += self.wv[edge[2]]

	def cal_cen(self,now):
		tmp = list()
		s1 = 0.0
		s2 = 0.0
		tmp.append(now)
		l = len(self.links[now])
		for i in self.links[now]:
			tmp.append(i[0])
			s1 += self.CC[i[0]]
		s2 = 0
		for i in tmp:
			for j in self.links[i]:
				if j[0] in tmp:
					s2 += self.wv[j[1]]
		return [s1/self.sum_node,s2/self.sum_edge]


	def cal_CC(self):
		v1 = list()
		v2 = list()
		for i in range(CT.pnum):
			if i in CT.bed or i in CT.good:
				continue
			v1.append(self.AA[i])
			v2.append(self.BB[i])
		v3 = self.cal_topsis(v1,v2)
		print '???',len(v1),' ',len(v2),' ',len(v3)
		k = 0
		for i in range(CT.pnum):
			if i in CT.bed:
				self.CC[i] = 1
			elif i in CT.good:
				self.CC[i] = 0
			else:
				self.CC[i] = v3[k]
				k += 1
		self.sum_node = sum(self.CC)

	def cal_all_cen(self):
		for i in range(CT.pnum):
			[self.c1[i],self.c2[i]] = self.cal_cen(i)
		self.c3 = self.cal_topsis(self.c1,self.c2)

	def cal_rank(self):
		self.get_fri()
		self.get_AB()
		#print self.A
		#print self.BB
		self.cal_CC()
		self.cal_all_cen()
		rank = list()
		for i in range(CT.pnum):
			if not i in CT.bed:
				rank.append(man(self.name[i], i, self.AA[i], self.BB[i], self.CC[i], self.c1[i], self.c2[i], self.c3[i], self.gorb(i)))
		rank.sort(cmp_val)
		for i in range(len(rank)):
			rank[i].pri3(i+1)
		self.v = [0 for i in range(CT.pnum)]


A = DealData()
A.get_data()
A.get_send()
#print A.send
A.cal_wv()
A.get_dv()
A.cal_A()
#print "_______",A.A
A.cal_B()
A.cal_rank()
