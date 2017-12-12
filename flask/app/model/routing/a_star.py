# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 15:50:29 2017

@author: Admin
"""
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

def astar_max_distance(graph, source, target, percent_shortest_path, 
                       ele_heuristic, len_heuristic):
    push = heappush
    pop = heappop
    counter = count()
    shortest_path = nx.shortest_path_length(graph, source, target, 'length')
    max_length = shortest_path * percent_shortest_path
    
    #(priority, counter, path_ele_gain, path_length, cur_node, path)
    pqueue = [(0, next(counter), 0, 0, source, [])]
    
    #
    while pqueue:
        _, __, path_ele_gain, path_length, cur_node, path = pop(pqueue)
        
        if cur_node == target:
            return path
        
        for neighbor, data in graph[cur_node].items():
            for key, weights in data.items():
                
                # New weights
                new_path_length = path_length + weights['length']
                new_path_ele_gain = path_ele_gain + weights['ele_gain']
                
                # No retracing
                if (neighbor, cur_node, key) in path or (cur_node, neighbor, key) in path:
                    continue
                
                # Prune any paths which will end up longer than desired
                est_length = new_path_length + len_heuristic(graph, neighbor, target)
                if est_length > max_length:
                    continue
                
                # Otherwise, add neighbor
                priority = new_path_ele_gain + ele_heuristic(graph, neighbor, target)
                new_path = path[:]
                new_path.append((neighbor, key))
                push(pqueue, (priority, next(counter), new_path_ele_gain, 
                              new_path_length, neighbor, new_path))
            

"""
source = #id
target = #id
print('source:', source, 'target:', target)
print(astar_max_distance(city, source, target, 1.5, elevation_heuristic, length_heuristic))
"""



