def build_adjacency_list(nodes, edges_text):
    """Parses raw text input into an adjacency list."""
    adjList = [[] for _ in range(nodes + 1)]
    
    if not edges_text.strip():
        return adjList
        
    lines = edges_text.strip().split('\n')
    for line in lines:
        if line.strip():
            c1, c2 = map(int, line.split())
            adjList[c1].append(c2)
            adjList[c2].append(c1)
            
    return adjList