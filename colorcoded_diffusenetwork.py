import networkx as nx
import json
import matplotlib.pyplot as plot

#open toxic classification json
with open('climate_change_posts_toxic.json', 'r') as f:
    posts = json.load(f)
graph = nx.Graph()

#iterate and add user to node and color code
#green = not toxic, red = toxic
for post in posts:
    user_id = post['user']
    graph.add_node(user_id)
    if post.get('toxic'):
        graph.nodes[user_id]['color'] = 'red'
    else:
        graph.nodes[user_id]['color'] = 'green'

node_colors = [graph.nodes[node]['color'] for node in graph.nodes]

#construct graph
plot.figure(figsize=(12, 12))
pos = nx.spring_layout(graph)
nx.draw(graph, pos, with_labels=True, node_color=node_colors, node_size=100, font_size=8, width=1.0)
plot.title("Info Diffuse Toxicity Netowrk (Red = Toxic, Green = Not Toxic)")
plot.show()