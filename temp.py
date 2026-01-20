import random 
# Define the decision tree as a dictionary
tree = {
    'A': [],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F', 'G'],
    'D': ['H', 'B'],
    'E': ['B', 'I'],
    'F': ['C', 'J', 'K'],
    'G': ['C', 'L'],
    'H': ['D'], 'I': ['E'], 'J': ['F','K'], 'K': ['J','F'],
    'L': ['G','M'], 'M': ['L'], 
    'N': ['O'], 'O': [], 'P': ['O']
}

blocked = ['A', 'O']

def find_end_nodes( blocked):
        endNodes = []
        nodes = ['A', 'H', 'I', 'M', 'N', 'O', 'P']
        for node in nodes:
            if nodes.count(node) == 1 and node not in blocked:
                endNodes.append(node)
        return endNodes

def get_current_adjacent_nodes(node, roads):
        adjacentNodes = []
        for road in roads:
            if road[0] == node:
                adjacentNodes.append(road[1])
            elif road[1] == node:
                adjacentNodes.append(road[0])
        return adjacentNodes

def dfs_max_length_one_chain(tree:dict, node, visited:list=None, depth:int=0, maxDepth:int=0):
    if not visited:
        visited = []
    visited.append(node) # mark node as visited
    for child in tree[node]:  # recursively visit children
        if child not in visited:
            childDepth = dfs_max_length_one_chain(tree,child,visited.copy(), depth+1, max(maxDepth,depth+1))
            # visited is a copy so that is doesnt change every instance of visited and effect the loop
            maxDepth=max(maxDepth, childDepth)
    return maxDepth

def dfs_max_length(tree, blocked=blocked):
    longestPlayerRoad = 0
    endNodes = find_end_nodes(blocked)
    for node in endNodes:
        longestPlayerRoad = max(longestPlayerRoad, dfs_max_length_one_chain(tree, node))
    return longestPlayerRoad

# Run DFS starting from node 'A'
print(dfs_max_length(tree))
