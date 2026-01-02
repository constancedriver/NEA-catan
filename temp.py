def split_locations(roads):
    components = []
    for road in roads:
        a, b = road
        placed = False
        for comp in components:
            if any(a in r or b in r for r in comp):
                comp.append(road)
                placed = True
                break
        if not placed:
            components.append([road])
    return components

def merge_components(roads):
    components = split_locations(roads)
    merged = True
    while merged:
        merged = False
        for i in range(len(components)):
            for j in range(i + 1, len(components)):
                if any(a in r or b in r for r in components[i] for a, b in components[j]):
                    components[i].extend(components[j])
                    components.pop(j)
                    merged = True
                    break
            if merged:
                break
    return components

#Depth first search
def dfs(node, used_roads, used_nodes, components, blocked_nodes):
        max_len = 0
        for i, (a, b) in enumerate(components):
            if i in used_roads:
                continue
            if a == node or b == node:
                next_node = b if a == node else a
                if next_node in blocked_nodes or next_node in used_nodes:
                    continue
                used_roads.add(i)
                used_nodes.add(next_node)
                max_len = max(max_len, 1 + dfs(next_node, used_roads, used_nodes, components, blocked_nodes))
                used_roads.remove(i)
                used_nodes.remove(next_node)
        return max_len

def find_longest(components, blocked_nodes):
    longest = 0
    for comp in components:
    # Count degree of each intersection
        degree = {}
        for a, b in comp:
            if a not in blocked_nodes:
                degree[a] = degree.get(a, 0) + 1
            if b not in blocked_nodes:
                degree[b] = degree.get(b, 0) + 1

        # Find endpoints (degree 1 nodes)
        endpoints = [node for node, d in degree.items() if d == 1]

        # Case 1: Pure loop (no endpoints, all degree 2)
        if endpoints == [] and degree and all(d == 2 for d in degree.values()):
            longest = max(longest, len(comp))
            continue

        # Case 2: Path or loop with tail
        # Start DFS from all endpoints
        if endpoints:
            for node in endpoints:
                longest = max(longest, dfs(node, set(), {node}, comp))
        else:
            # Loop with a tail, or internal loop: start DFS from every node
            for node in degree.keys():
                longest = max(longest, dfs(node, set(), {node}, comp))

    return longest

def longest_road_chain(road_locations,blocked_nodes):
    return find_longest(road_locations,blocked_nodes)

###test####
    
roads = [((3,4,0), (3,3,0)), ((3,4,0), (3,4,-1)), ((3,4,0), (4,4,0)), ((0,1,0), (1,1,0)), ((1,1,0), (1,1,1)), ((1,1,1), (2,1,1)), ((2,1,1), (2,1,2)), ((2,1,2), (2,0,2)), ((2,0,2), (1,0,2)), ((1,0,2), (1,0,1)), ((1,0,1), (1,1,1)), ((2,1,1), (2,2,1)), ((2,2,1), (3,2,1))]
blocked = []

    # Calculate the longest legal road
print("Longest Road Length:", longest_road_chain(roads, blocked))
