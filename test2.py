import networkx as nxx
import csv
import matplotlib.pyplot as plt
import math
import random

def cmp_size(a, b):
    return cmp(b.node_size, a.node_size)

class nod():
    def __init__(self,node_size,node_id):
        self.node_size = node_size
        self.node_id = node_id
        self.color = 'r'


g = nxx.Graph()
g.add_nodes_from([0,1])

nxx.draw_networkx(g,pos=[[0,0],[1000,0]],node_size=[100000,1000])
plt.savefig('test2.png')
