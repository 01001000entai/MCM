import math
import numpy as np
import networkx as nx

a = np.matrix([[0 for i in range(20)] for j in range(20)], dtype=np.float)
a[0,12] = 1
a[4,5] = 1
a[8,18] = 1
a[10,0] = 1
a[10,1] = 1
a[10,2] = 1
a[10,3] = 1
a[10,7] = 1
a[10,8] = 1
a[10,9] = 1
a[10,12] = 1
a[10,13] = 1
a[10,17] = 1
a[10,18] = 1
a[10,19] = 1
a[12,10] = 1
a[14,3] = 1
a[14,5] = 1
a[14,13] = 1

g = nx.DiGraph()
g.add_nodes_from(range(21)[1:21])
for i in range(20):
	for j in range(20):
		if a[i,j] > 0:
			g.add_edge(i+1,j+1)
nx.write_pajek(g,'g3.net')


print a
year = [1959,2002,1987,1999,2006,
		2000,1979,2000,2001,2001,
		2003,2007,2002,1998,2011,
		1996,1996,1987,1993,2000]

b = np.matrix([
	0.459,41.766,1.348,30.486,0.578,
	2.138,3.277,36.540,2.359,9.635,
	5.578,2.783,30.4865,36.5405,3.63,
	2.138,7.9,0.459,7.528,9.635,
	], dtype=np.float)
s = 0.0
for i in range(20):
	s += b[0,i]
b /= s
print b
def dis(a,b):
	return year[a] - year[b]

p = 0.15
for i in range(20):
	s = 0.0
	for j in range(20):
		s += a[i,j]
	print 'hehehe',s
	if s == 0:
		a[i,i] = 1
	else:
		tmp = np.array([0.0 for t in range(20)], dtype=np.float)
		for j in range(20):
			if a[i,j] > 0:
				print "kkk~~~~~~"
				tmp[j] = math.e**(-dis(i,j))
		s = 0
		print tmp
		print s
		for j in range(20):
			s += tmp[j]
		for j in range(20):
			if i == j:
				a[i,j] = p
			else:
				print 'lll ', len(tmp),' ',i,' ',j,' ',a[i,j]
				a[i,j] = (1-p)*(tmp[j]/s)

print a
print b * a**100