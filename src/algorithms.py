import copy
from queue import Queue

def expandLevel(nodeQueue, adjList, ancestor, visited, visitedFlag):
    oppositeFlag = visitedFlag * (-1)
    size = nodeQueue.qsize()
    for i in range(size):
        node = nodeQueue.get()
        for padosi in adjList[node]:
            if visited[padosi] == 0:  
                visited[padosi] = visitedFlag
                nodeQueue.put(padosi)
                ancestor[padosi] = node
            elif visited[padosi] == oppositeFlag:  
                return [padosi, node, visitedFlag]
    return []

def backtrackAndBuildPath(ancestor, start, end):
    path = []
    while start != end:
        path.append(start)
        start = ancestor[start]
    path.append(end)
    return path

def bidirectional_bfs(nodes, adjList, source, destination):
    visited = [0 for _ in range(nodes + 1)]
    ancestor = [0 for _ in range(nodes + 1)]
    forwardQueue = Queue()
    backwardQueue = Queue()

    forwardQueue.put(source)
    visited[source] = 1
    backwardQueue.put(destination)
    visited[destination] = -1
    
    history = []
    # Snapshot 0: Initial State
    history.append({"visited": copy.deepcopy(visited), "path": []})
    
    res = []
    while True:
        # Expand Forward & Snapshot
        res = expandLevel(forwardQueue, adjList, ancestor, visited, 1)
        history.append({"visited": copy.deepcopy(visited), "path": []})
        if len(res) > 0: break
        
        # Expand Backward & Snapshot
        res = expandLevel(backwardQueue, adjList, ancestor, visited, -1)
        history.append({"visited": copy.deepcopy(visited), "path": []})
        if len(res) > 0: break

    direction = res[2]
    if direction == 1:
        srcpath = backtrackAndBuildPath(ancestor, res[1], source)
        destpath = backtrackAndBuildPath(ancestor, res[0], destination)
    else:
        srcpath = backtrackAndBuildPath(ancestor, res[0], source)
        destpath = backtrackAndBuildPath(ancestor, res[1], destination)
        
    srcpath.reverse()
    finalpath = srcpath + destpath    
    
    # Final Snapshot: Path Found
    history.append({"visited": copy.deepcopy(visited), "path": finalpath})
    return history

def unidirectional_bfs(nodes, adjList, source, destination):
    q = Queue()
    q.put(source)
    visited = [0 for _ in range(nodes + 1)]
    visited[source] = 1
    ancestor = [0 for _ in range(nodes + 1)]
    ancestor[source] = source
    
    history = []
    # Snapshot 0: Initial State
    history.append({"visited": copy.deepcopy(visited), "path": []})
    
    found = False
    while q.qsize() > 0:
        node = q.get()
        for padosi in adjList[node]:
            if visited[padosi] == 0:
                visited[padosi] = 1
                ancestor[padosi] = node
                q.put(padosi)
                if padosi == destination:
                    found = True
                    break
        
        # Snapshot after expanding a node's neighbors
        history.append({"visited": copy.deepcopy(visited), "path": []})
        if found: break
                    
    path = backtrackAndBuildPath(ancestor, destination, source)
    path.reverse()
    
    # Final Snapshot: Path Found
    history.append({"visited": copy.deepcopy(visited), "path": path})
    return history