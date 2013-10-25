import networkx as nx
import matplotlib.pyplot as plt
#from matplotlib import animation

class Particle:
  current_node = None
  def __init__(self, node):
    self.current_node = node

G=nx.DiGraph()

G.add_weighted_edges_from([(1,2,.05),(3,1,0.75),(1,0,.1),(3,4,.2),(3,2,.4),(2,3,.3)])
particle_list = [Particle(node) for node in G.nodes()]
for particle in particle_list:
  G.node[particle.current_node]['particles'] = [particle]

weights = []
for edge in G.edges():
  weights.append(G[edge[0]][edge[1]]['weight'])
  
pos = nx.random_layout(G)
plt.figure(figsize=(8,8))
nx.draw_networkx_edges(G,pos,edge_color=weights,
                        alpha=0.4,edge_cmap=plt.cm.jet,
                        edge_vmin=min(weights),edge_vmax=max(weights))

occupancy = [len(G.node[n]['particles']) for n in G.nodes()]
node_weights = { n:particles for n,particles in zip(G.nodes(),occupancy) }

nx.draw_networkx_nodes(G,pos,
                       node_color=node_weights.values(),
                       cmap=plt.cm.jet,
                       vmin=min(node_weights.values()),
                       vmax=max(node_weights.values()))
plt.show()
