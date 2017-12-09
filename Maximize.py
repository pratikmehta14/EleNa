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

def maximize(graph, source, target, percent_shortest_path,
                       ele_heuristic, len_heuristic):
    push = heappush
    pop = heappop
    counter = count()
    shortest_path = nx.shortest_path_length(graph, source, target, 'length')
    max_length = shortest_path * percent_shortest_path

    