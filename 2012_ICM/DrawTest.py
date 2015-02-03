import networkx as nxx
import csv
import matplotlib.pyplot as plt
import CT

g = [nxx.DiGraph() for i in range(CT.tpnum)]

d = csv.reader(file('Names.csv'))

name = ['' for i in range(CT.pnum)]

for line in d:
	if d.line_num == 1:
		continue
	if line[0] != '':
		name[int(line[0])] = line[1]
	print line[0]
	for i in range(CT.tpnum):
		g[i].add_node(int(line[0]))

d = csv.reader(file('Messages.csv'))

for line in d:
	print line 
	if d.line_num == 1:
		continue
	for i in range(2,5):
		print 'i:',i,' ',line[i]
		if line[i] != '' and int(line[i]) <= 15:
			g[int(line[i])-1].add_edge(int(line[0]),int(line[1]))

for i in range(CT.tpnum):
	plt.figure(figsize=(25,25))
	node_color = ['b' for j in range(CT.pnum)]
	for j in range(CT.pnum):
		if j in CT.bed:
			node_color[j] = 'r'
		if j in CT.good: 
			node_color[j] = 'y'
	nxx.draw(g[i], node_color=node_color,with_labels=True)
	plt.savefig('fig%d.png' % (i+1))
	plt.cla()

