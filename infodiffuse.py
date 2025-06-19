import networkx as nx
import json
import matplotlib.pyplot as plot

#open posts json
with open('climate_change_posts.json', 'r') as f:
    posts = json.load(f)
graph = nx.DiGraph()

#add nodes
for post in posts:
    #unique post id is combination of username and time post was created
    #this is how to differentiate between nodes since users can post multiple times and things can be posted at the same time
    #then add content of post and user data to the node (not shown due to too much info being visualized)
    post_id = post['user'] + ' ' + str(post['created_at'])
    graph.add_node(post_id, content=post['content'], user=post['user'])

    #check for info propagation to see if post was replied or boosted
    #add directed edges for each case
    #if post is a reply, edge drawn from original to post
    #if post is a boost of another, edge drawn from original to post
    if 'in_reply_to_id' in post and post['in_reply_to_id']:
        graph.add_edge(post['in_reply_to_id'], post_id)  
    elif 'boosted_post_id' in post and post['boosted_post_id']:
        graph.add_edge(post['boosted_post_id'], post_id)  

#construct
plot.figure(figsize=(10, 10))
nx.draw(graph, with_labels=False, node_size=30, font_size=10, arrows=True)
plot.title("Information Diffusion Network")
plot.show()