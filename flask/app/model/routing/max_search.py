"""
 Elevation gain maximization algorithm within x% of shortest path

 @author: Benjamin Guinsburg
"""

import networkx as nx
import copy


def find_path_edges(graph, path, max_weight='ele_gain'):
	"""
    Given a path as a list of nodes, and the weight to maximize, finds the 
    edges that will maximize the weight between each node in the list. For 
    convieniece this function returns the length and elevation gain found along
    all of these edges, in addition to the list of keys that corisponds to 
    these edges.
        
    Parameters:
    -----------
    graph: NetworkX MultiDiGraph
        The graph that this path belongs to.
    path: list of int
        Each int should represent a node id in the graph along a path.
    min_weight: string
        The weight that will be maximized along the path.
        
    Returns: 
    --------
    path_length: float
        The total distance along every edge found
    path_ele_gain: float
        The total elevation gain along every edge found
    path_edge_keys: list of int
        Each int represents the key of the edge between two consecutive nodes 
        in path which minimizes min_weight.        
	"""    
	path_length = 0
	path_ele_gain = 0
	path_edge_keys = []
	for i in range(len(path) - 1):
		edges = graph[path[i]][path[i + 1]]
		min_weight_edge = max(edges.keys(), key=lambda k: edges[k][max_weight])
		path_length += edges[min_weight_edge]['length']
		path_ele_gain += edges[min_weight_edge]['ele_gain']
		path_edge_keys.append(min_weight_edge)
	return (path_length, path_ele_gain, path_edge_keys)

def edge_path(node_path, edge_keys):
	"""
    Given a path as a list of nodes, and the key representing the edge between
    each node in the list, returns the path as a list of edges in the form
    (u, v, key).
    
    Parameters:
    -----------
    node_path: list of int
        Each int should represent a node id in the graph along a path.
    edge_keys: list of int
        Each int should represent the key of the edge between two nodes in
        node_path.
        
    Returns: 
    --------
    edge_path: list of (int, int, int)
        Each tuple (u, v, key) in the list represents an edge in the graph:
        graph[u][v][key].
	"""
	edge_path = []
	for i in range(len(node_path) - 1):
		edge_path.append((node_path[i], node_path[i + 1], edge_keys[i]))
	return edge_path


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

    alternate_paths_list = []

    #loop over nodes in the path to build alternate_paths_dict
    for i in range(len(shortest_path)-1):
        currentNode = shortest_path[i]
        nextNode = shortest_path[i+1]

        print("got currentNode = %d, and nextNode = %d, at iteration %d" % (currentNode, nextNode, i))

        #remove all nodes except currentNode and nextNode for the graph for this function
        graph_truncated = copy.deepcopy(graph)
        graph_truncated.remove_nodes_from(shortest_path[0:i] + shortest_path[i + 2:])
        interPaths = nx.all_simple_paths(graph_truncated, currentNode, nextNode, cutoff=10)

        #find path in interPaths that has highest ele-gain
        ele_gain_max = 0
        path_length = 0
        biggestPath = []

        for path in interPaths:
            ele_gain, length, _ = find_path_edges(graph, path)

            if (ele_gain < 0): continue

            if (ele_gain > ele_gain_max):
                ele_gain_max = ele_gain
                path_length = length
                biggestPath = path

        biggest_path_length = len(biggestPath)

        if (path_length != 0 and biggest_path_length != 2):
            alternate_paths_list.append( (ele_gain_max/path_length, path_length, biggestPath, currentNode, nextNode) )


    alternate_paths_list.sort(key=lambda  tup: tup[0], reverse=True)

    #loop over alternate_paths_list, and insert into working path
    for tuple in alternate_paths_list:
        working_path = insertPath(graph, working_path, tuple[1], tuple[2], tuple[3], tuple[4], max_length)

    best_dist, best_gain, best_keys = find_path_edges(graph, working_path)
    best_path = edge_path(working_path, best_keys)
    return (best_dist, best_gain, best_path)


def insertPath(graph, working_path, path_length, path, node1, node2, max_length):
    node1_ind = working_path.index(node1)
    node2_ind = working_path.index(node2)

    if path_length > max_length:
        return working_path
    else:
        return working_path[0:node1_ind] + path + working_path[node2_ind + 1:]