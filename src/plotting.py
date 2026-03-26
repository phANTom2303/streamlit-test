import networkx as nx
import matplotlib.pyplot as plt

def generate_graph_figure(adjList, visited, path, title):
    G = nx.Graph()
    for i in range(1, len(adjList)):
        G.add_node(i)
        for neighbor in adjList[i]:
            G.add_edge(i, neighbor)
            
    pos = nx.spring_layout(G, seed=42) 
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    valid_nodes = range(1, len(adjList))
    nx.draw_networkx_nodes(G, pos, nodelist=valid_nodes, node_color='lightgray', node_size=300, ax=ax)
    
    forward_visited = [i for i in range(1, len(visited)) if visited[i] == 1 and i not in path]
    backward_visited = [i for i in range(1, len(visited)) if visited[i] == -1 and i not in path]
    
    # Only draw categories if they exist in this frame
    if forward_visited:
        nx.draw_networkx_nodes(G, pos, nodelist=forward_visited, node_color='lightgreen', label='Forward Search', node_size=300, ax=ax)
    if backward_visited:
        nx.draw_networkx_nodes(G, pos, nodelist=backward_visited, node_color='orange', label='Backward Search', node_size=300, ax=ax)
    if path:
        nx.draw_networkx_nodes(G, pos, nodelist=path, node_color='red', label='Final Path', node_size=400, ax=ax)
    
    nx.draw_networkx_edges(G, pos, edge_color='gray', ax=ax)
    
    if path:
        path_edges = list(zip(path, path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2, ax=ax)
        
    nx.draw_networkx_labels(G, pos, font_size=8, ax=ax)
    
    ax.set_title(title)
    
    # Prevent legend warning if no elements have labels yet
    handles, labels = ax.get_legend_handles_labels()
    if handles:
        ax.legend(scatterpoints=1, bbox_to_anchor=(1.05, 1), loc='upper left') 
    
    return fig