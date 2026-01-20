import random

class calculateLongestRoad():
    def __init__(self, roads:list, blocks:list, roadsExplored:list=[], currentChainLength:int=0, longestChainLength:int=0, tree:dict={}):
        self.roads = roads
        self.blocks = blocks
        self.roadsExplored = roadsExplored
        self.currentChainLength = currentChainLength
        self.longestChainLength = longestChainLength
        self.tree = tree

    def get_nodes(self):
        nodes = []
        for road in self.roads:
            nodes.append(road[0])
            nodes.append(road[1])
        return nodes

    def find_end_nodes(self):
        endNodes = []
        nodes = self.get_nodes()
        for node in nodes:
            if nodes.count(node) == 1:
                endNodes.append(node)

    def get_current_adjacent_nodes(self,node):
        adjacentNodes = []
        for road in self.roads:
            if road[0] == node:
                adjacentNodes.append(road[1])
            elif road[1] == node:
                adjacentNodes.append(road[0])
        return adjacentNodes

    def create_tree(self):
        nodes = self.get_nodes()
        for node in nodes:
            self.tree.update({node: self.get_current_adjacent_nodes(node)})


    

#def dfs_recursive(graph, node, visited=set()):
#   if node not in visited:
#       visited.add(node)
#       print(node)  # Process the node
#
#       for neighbor in graph.get(node, []):
#           dfs_recursive(graph, neighbor, visited)