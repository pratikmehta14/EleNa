"""
 Elevation gain maximization algorithm within x% of shortest path

 @author: Benjamin Guinsburg
"""

import networkx as nx
import copy


"""
Given a graph, networkx will generate the shortest path P from source to target based on length.

It will then loop over the nodes P, and for each node it will  create a list L of all paths 
from P_n to P_n+1 with some cutoff depth. 
The graph handed to nx.all_simple_paths will have had all nodes P_0 through P_n-1 removed [IMPORTANT].
It loops over L to find the path that has the properties:
    1. ele_gain >= 0
    2. length(P_0 -> P_n) + length(L[i]) + length(P_n+1 -> P_k)
    3. L[i] has highest ele_gain in L
    
Upon finding this path P_new, it will be inserted between P_n and P_n+1 
"""
def maximize(graph, source, target, percent_shortest_path,):
    shortest_path = nx.shortest_path(graph, source, target, 'length')
    working_path = copy.deepcopy(shortest_path)

    shortest_path_len = nx.shortest_path_length(graph, source, target, 'length')
    max_length = shortest_path_len * percent_shortest_path

    #while we can still maximize ele-gain..
    # while (pathLength(graph, working_path) < max_length):

    offset = 0

    #loop over nodes in the path
    for i in range(len(shortest_path)-1):
        currentNode = shortest_path[i]
        nextNode = shortest_path[i+1]

        #remove all nodes except currentNode and nextNode for the graph for this function
        graph_truncated = copy.deepcopy(graph)
        graph_truncated.remove_nodes_from(shortest_path[0:i]+shortest_path[i+2:])
        interPaths = nx.all_simple_paths(graph_truncated, currentNode, nextNode, cutoff=10)

        #find path in interPaths that has highest ele-gain
        ele_gain_max = 0
        biggestPath = []

        for path in interPaths:
            ele_gain=0

            for node in range(len(path)-1):
                ele_gain += graph[path[node]][path[node + 1]][0]['ele_gain']

            if (ele_gain < 0): continue

            #if the whole new path is longer than allowed, disregard it
            if (pathLength(graph, working_path[0:offset] + path + working_path[offset+2:]) > max_length):
                continue

            if (ele_gain > ele_gain_max):
                ele_gain_max = ele_gain
                biggestPath = path

        biggest_path_length = len(biggestPath)
        if (biggest_path_length == 0):
            biggestPath = [currentNode, nextNode]
            biggest_path_length += 2
        working_path = working_path[0:offset] + biggestPath + working_path[offset+2:]
        offset += biggest_path_length - 1

    return working_path


def pathLength(graph, path):
    path_length = 0
    for node in range(len(path) - 1):
        path_length += graph[path[node]][path[node + 1]][0]['length']
    return path_length