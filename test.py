import matplotlib.pyplot as plt
import networkx as nx

# Dummy Data
drivers = ["Hamilton", "Verstappen", "Alonso"]
constructors = ["Mercedes", "Red Bull", "Ferrari"]
edges = [
    ("Hamilton", "Mercedes"),
    ("Verstappen", "Red Bull"),
    ("Alonso", "Ferrari"),
    ("Hamilton", "Ferrari")  # Hypothetical transfer
]

# Create bipartite graph
B = nx.Graph()
B.add_nodes_from(drivers, bipartite=0)
B.add_nodes_from(constructors, bipartite=1)
B.add_edges_from(edges)

# Position nodes in two columns
pos = {node: (0, i) for i, node in enumerate(drivers)}
pos.update({node: (1, i) for i, node in enumerate(constructors)})

# Draw
nx.draw(B, pos, with_labels=True, node_color=["skyblue"]*len(drivers) + ["lightgreen"]*len(constructors), node_size=2000)
plt.title("Driver-Constructor Bipartite Graph")
plt.show()