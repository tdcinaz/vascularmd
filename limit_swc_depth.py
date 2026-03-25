# This file should load centerline data from an swc file, traverse the tree structure and limit the depth of the tree to a specified value. The resulting tree should then be outputted as a new swc file.
import numpy as np
import networkx as nx

from ArterialTree import ArterialTree

# Import centerline data to create a networkx graph
# Import from swc file
centerline_filename = "Data/P1_whole_brain_BraVa.swc"

# Create a networkx graph from the swc file
def swc_to_graph(swc_file):
    G = nx.DiGraph()
    with open(swc_file, 'r') as f:
        for line in f:
            if line.startswith('#'):
                continue
            parts = line.strip().split()
            if len(parts) < 7:
                continue
            node_id = int(parts[0])
            node_type = int(parts[1])
            x = float(parts[2])
            y = float(parts[3])
            z = float(parts[4])
            radius = float(parts[5])
            parent_id = int(parts[6])
            G.add_node(node_id, type=node_type, x=x, y=y, z=z, radius=radius)
            if parent_id != -1:
                G.add_edge(parent_id, node_id)
    return G

# Limit the depth of the tree to a specified value
def limit_tree_depth(G, max_depth):
    root = [n for n, d in G.in_degree() if d == 0][0]  # Find the root node
    limited_G = nx.DiGraph()
    def dfs(node, depth):
        if depth > max_depth:
            return
        limited_G.add_node(node, **G.nodes[node])
        for neighbor in G.successors(node):
            if depth + 1 <= max_depth:
                dfs(neighbor, depth + 1)
                limited_G.add_edge(node, neighbor)
    dfs(root, 0)
    return limited_G

# Convert the swc file to a graph
G = swc_to_graph(centerline_filename)

# Limit the depth of the tree to a specified value (e.g., 40)
max_depth = 40
limited_G = limit_tree_depth(G, max_depth)

# Convert the limited graph back to an swc file
def graph_to_swc(G, output_file):
    with open(output_file, 'w') as f:
        for node in G.nodes(data=True):
            node_id = node[0]
            data = node[1]
            node_type = data['type']
            x = data['x']
            y = data['y']
            z = data['z']
            radius = data['radius']
            parent_id = -1
            for predecessor in G.predecessors(node_id):
                parent_id = predecessor
                break
            f.write(f"{node_id} {node_type} {x} {y} {z} {radius} {parent_id}\n")

# Output the limited tree as a new swc file
output_swc_file = "Data/limited_tree.swc"
graph_to_swc(limited_G, output_swc_file)