import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

# take a adjacency matrix
#G = nx.from_numpy_arry(a)
#nx.eigenvector_centrality(G)
plt.figure('ya')
G = nx.Graph()
G.add_nodes_from(['1', '2','3','4','5a','5b','6','7','8','9','Reb1','Reb2','Reb3','Cond1','Cond2','Cond3'])
G.add_weighted_edges_from([
    ('1', '2', 650.99), 
    ('1', 'Cond3', 192.25),
    ('1','Cond2', 143.75),
    ('2','Reb2', 55.88),
    ('2','Reb1', 28.5),
    ('3', 'Cond2', 43.05),
    ('7','Reb2', 74.65),
    ('7','Reb1', 66.5),
    ('8','Reb2', 10.68),
    ('Reb2','Cond3', 145.29)
])
print(G.nodes())
print(G.edges())

central = nx.eigenvector_centrality_numpy(G,weight='weight')
for key in central:
    print('{}    {:.4g}'.format(key, central[key]))

pos=nx.spring_layout(G)
nx.draw_networkx_nodes(G,pos,
                       nodelist=['1','2'],
                       node_color='darkblue',
                       node_size=500,
                    alpha=0.8)
nx.draw_networkx_nodes(G,pos,
                       nodelist=['Cond2','Reb2','Cond3'],
                       node_color='blue',
                       node_size=500,
                    alpha=0.8)
nx.draw_networkx_nodes(G,pos,
                       nodelist=['Reb1','7'],
                       node_color='royalblue',
                       node_size=500,
                    alpha=0.8)
nx.draw_networkx_nodes(G,pos,
                       nodelist=['3','8'],
                       node_color='lightsteelblue',
                       node_size=500,
                    alpha=0.8)
nx.draw_networkx_edges(G,pos,
                       edgelist=[
    ('2','Reb2'),
    ('2','Reb1'),
    ('3', 'Cond2'),
    ('7','Reb2'),
    ('7','Reb1'),
    ('8','Reb2'),
],
                       width=1,alpha=1,edge_color='grey')
nx.draw_networkx_edges(G,pos,
                       edgelist=[
    ('1', '2')
],
                       width=5,alpha=1,edge_color='grey')
nx.draw_networkx_edges(G,pos,
                       edgelist=[
    ('1', 'Cond3'),
    ('1','Cond2'),
    ('Reb2','Cond3')
],
                       width=3,alpha=1,edge_color='grey')             
labels={}
labels['1']=r'$1$'
labels['2']=r'$2$'
labels['3']=r'$3$'
labels['4']=r'$4$'
labels['5a']=r'$5a$'
labels['6']=r'$6$'
labels['7']=r'$7$'
labels['8']=r'$8$'
labels['9']=r'$9$'
labels['5b']=r'$5b$'
labels['Reb1']='Reb1'
labels['Reb2']='Reb2'
labels['Reb3']='Reb3'
labels['Cond1']='Cond1'
labels['Cond2']='Cond2'
labels['Cond3']='Cond3'
#nx.draw_networkx_labels(G,pos,labels,font_size=16,font_color='gold')

plt.axis('off')
plt.show()