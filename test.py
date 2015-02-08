import networkx as nxx
import csv
import matplotlib.pyplot as plt
import math
import random

color = ['r','y','b','g']

def cmp_size(a, b):
    return cmp(b.node_size, a.node_size)

class nod():
    def __init__(self,node_size,node_id):
        self.node_size = node_size
        self.node_id = node_id
        self.color = 'r'

nd = list()
pos = [[0,0] for i in range(30)]
g = nxx.gnm_random_graph(30,100)
node_size = [(2**(4+nxx.degree(g,i))+200)*2 for i in g]
for i in g:
    nd.append(nod(node_size[i],i))

nd.sort(cmp_size)

print [nd[i].node_size for i in range(30)]

color = ['r' for i in range(30)]
rest = 0
num_node_cir = 2
le = 400.0
col = 0
for (s,i) in enumerate(nd):
    if rest == 0:
        rest = num_node_cir
        num_node_cir *= 2
        le += 1500
        col += 1
        d = random.randint(0,180)
        dd = 360 / rest
    pos[i.node_id] = [le*math.cos(d), le*math.sin(d)]
    d += dd
    color[i.node_id] = col
    rest -= 1

label = ["AAADSA%d" % (i) for i in range(30)]



for i in g:
    g[i]['label'] = 'AAA%d' % (i)
print label
plt.figure(figsize=(40,40))
nxx.draw_networkx(g,pos=pos,node_size=node_size,node_color=color,font_size=10)
plt.savefig('test.png')
print [i/5 for i in range(30)]
