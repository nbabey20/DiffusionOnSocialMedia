import networkx as nx
import json
import matplotlib.pyplot as plot

#get users and create ghraph
with open('climate_change_users.json', 'r') as f:
    users = json.load(f)
graph = nx.Graph()

#iterate and create nodes and edges
for user in users:
    user_id = user['username']
    graph.add_node(user_id)
    #edges for friends
    if 'follows' in user and user['follows']:
        for followed_user_id in user['follows']:
            graph.add_edge(user_id, followed_user_id) 

#friendship network visuals
plot.figure(figsize=(12, 12))
pos = nx.spring_layout(graph)
nx.draw(graph, pos, with_labels=True, node_size=100, font_size=8, edge_color='black', width=1.0)
plot.title("Friendship Network")
plot.show()

#calculate local level 1 hop
node_degrees = dict(graph.degree())

#calc avg 1 hop
avg_1hop = sum(node_degrees.values()) / len(node_degrees)
print(f"Average number of 1hop friends: {avg_1hop}")
for node, degree in node_degrees.items():
    print(f"Node {node} has {degree} 1hop friends")

#global average num of friends
global_avg = sum(node_degrees.values()) / len(graph.nodes())
print(f"Global average number of friends: {global_avg}")

#calculate degree distribution
degree_num = sorted([d for n, d in graph.degree()], reverse=True)
plot.hist(degree_num, bins=10)
plot.title("Degree distribution")
plot.xlabel("Degree")
plot.ylabel("Frequency")
plot.show()

#clustering coefficient
clustering_coeff = nx.average_clustering(graph)
print(f"Average clustering coefficient: {clustering_coeff}")

#page rank calc
pagerank = nx.pagerank(graph)
node_sizes = [v * 10000 for v in pagerank.values()]  # Scale by multiplying by a factor
print(f"Page rank plotted in second graph with variable sizes depending on value")

#same graph for page rank
plot.figure(figsize=(12, 12))
nx.draw(graph, node_size=node_sizes, with_labels=True, font_size=8)
plot.title("Page rank graph (node size represents rank)")
plot.show()
