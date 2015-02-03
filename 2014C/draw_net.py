import networkx as nx

g = nx.Graph()
g.add_nodes_from(range(9)[1:9])
g.add_nodes_from(['A','B','C','D'])

g.add_edges_from([[1,2],[1,'D'],
			[2,'D'],[2,3],[2,5],[2,'A'],
			[3,'D'],[3,4],
			[4,'D'],
			[5,'A'],[5,'C'],
			[6,'A'],[6,'C'],
			[7,8],
			['A','C'],
			])

nx.write_pajek(g,'g6.net')