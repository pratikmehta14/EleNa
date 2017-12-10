import osmnx as ox, networkx as nx
from heapq import heappush, heappop
from itertools import count



def elevation_heuristic(graph, source, target):
    return max(0, graph.nodes[target]['elevation'] - graph.nodes[source]['elevation'])

def length_heuristic(graph, source, target):
    s_y = graph.nodes[source]['y']
    s_x = graph.nodes[source]['x']
    t_y = graph.nodes[target]['y']
    t_x = graph.nodes[target]['x']
    return ox.euclidean_dist_vec(s_y, s_x, t_y, t_x)

"""
Given a graph, networkx will generate the shortest path P from source to target based on length.
It will then loop over the nodes P, starting from the second to last, and for each node it will 
find all 
"""
def maximize(graph, source, target, percent_shortest_path,
                       ele_heuristic, len_heuristic):
    push = heappush
    pop = heappop
    counter = count()
    shortest_path = nx.shortest_path(graph, source, target, 'length')
    shortest_path_len = nx.shortest_path_length(graph, source, target, 'length')
    max_length = shortest_path_len * percent_shortest_path

    # for i in range(len(shortest_path)-1):














#modified version of networkx's function, modified so that cutoff is a function of distance
def all_simple_paths_multigraph(G, source, target, cutoff=None):
    if cutoff < 1:
        return
    visited = [source]
    stack = [(v for u, v in G.edges(source))]
    while stack:
        children = stack[-1]
        child = next(children, None)
        if child is None:
            stack.pop()
            visited.pop()
        elif len(visited) < cutoff:
            if child == target:
                yield visited + [target]
            elif child not in visited:
                visited.append(child)
                stack.append((v for u, v in G.edges(child)))
        else:  # len(visited) == cutoff:
            count = ([child] + list(children)).count(target)
            for i in range(count):
                yield visited + [target]
            stack.pop()
            visited.pop()
