import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

class Particle:
  current_node = None
  def __init__(self, node):
    self.current_node = node

G=nx.scale_free_graph(200)
for e in G.edges():
  G.edge[e[0]][e[1]]['weight']=np.random.random_sample()

particle_list = [Particle(node) for node in G.nodes()]
for particle in particle_list:
  G.node[particle.current_node]['particles'] = [particle]

weights = []
for e in G.edges():
  weights.append(G.edge[e[0]][e[1]]['weight'])
    
pos = nx.random_layout(G)

def animate(i):
  fig = plt.figure(figsize=(8,8))
  for particle in particle_list:
    n = particle.current_node
    successors = { successor:G.edge[n][successor]["weight"] for successor in G.neighbors(n) }
    total_weight = 0
    for successor, weight in successors.items():
      total_weight += weight
    rand = np.random.random_sample() * total_weight
    next_node = None
    for successor, weight in successors.items():
      rand -= weight
      if rand < 0:
        next_node = successor
        break
    if next_node is not None:
      G.node[particle.current_node]["particles"].remove(particle)
      G.node[next_node]["particles"].append(particle)
      particle.current_node = next_node

  nx.draw_networkx_edges(G,pos,edge_color=weights,
                          alpha=0.2,edge_cmap=plt.cm.jet,
                          arrows=False,
                          edge_vmin=min(weights),edge_vmax=max(weights))

  occupancy = [len(G.node[n]['particles']) for n in G.nodes()]
  node_weights = { n:particles for n,particles in zip(G.nodes(),occupancy) }

  nx.draw_networkx_nodes(G,pos,
                         node_color=node_weights.values(),
                         node_size=40,
                         alpha=.6,
                         cmap=plt.cm.jet,
                         vmin=min(node_weights.values()),
                         vmax=max(node_weights.values()))
  plt.axis("off")
  plt.savefig('figure#%s' %i)
  plt.close()
  return

if __name__ == "__main__":
  for i in range(20):
    animate(i)
