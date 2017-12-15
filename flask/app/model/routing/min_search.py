# -*- coding: utf-8 -*-
"""
Elevation gain minimization algorithms within x% of shortest path

@author: Jeremy Doyle
"""
import networkx as nx, osmnx as ox


def find_path_edges(graph, path, min_weight='grade'):
	"""
    Given a path as a list of nodes, and the weight that was used when finding 
    the shortest path, finds the edge that was used to minimize the weight 
    between each node in the list. For convieniece this function returns the 
    length and elevation gain found along all of these edges, in addition to 
    the list of keys that corisponds to these edges.
        
    Parameters:
    -----------
    graph: NetworkX MultiDiGraph
        The graph that this path belongs to.
    path: list of int
        Each int should represent a node id in the graph along a path.
    min_weight: string
        The weight that was minimized when finding this path.
        
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
		min_weight_edge = min(edges.keys(), key=lambda k: edges[k][min_weight])
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



def minimize_elevation_gain(graph, source, target, percent_shortest_path, iterations=10):
	"""
    Minimizes elevation gain within constraint of x% of the shortest path by 
    performing a binary search over alpha(between 1.0 and 0.0) such that each 
    iteration calculates a new weight for every edge as the linear combination
    of alpha * normalized distance + (1 - alpha) * normalized elevation gain, 
    and finds the resulting shortest weighted path.
    
    Parameters:
    -----------
    graph: NetworkX MultiDiGraph
        The graph to perform the search on.
    source: int
        The node id of the source point.
    target: int
        The node id of the target point.
    percent_shortest_path: float (> 1.0)
        The constraint of the maximum distance allowed, represented as a 
        percentage of the shorted distance path (1.0 = 100%).
    iterations: int
        The maximum number of iterations of the binary search to perform, at 
        which point the algorithm will return the best path found thus far. 
        The default here is 10, which was found to be a decent trade-off 
        between runtime and result performance.
        
    Returns: 
    --------
    best_path_dist: float
        The total distance of the best path found
    best_path_gain: float
        The total elevation gain of the best path found
    best_edge_path: list of (int, int, int)
        Each tuple (u, v, key) in the list represents an edge in the graph:
        graph[u][v][key]. The resulting list of edges is the best path found to
        minimize elevation gain given the constraint        
	"""
	# Enforce x% of shortest path 1.0 or larger
	if percent_shortest_path < 1.0:
		raise Exception("Cannot find a path shorter than the shortest path.")
	
	# Find shortest distance path
	min_dist, min_dist_path = nx.single_source_dijkstra(graph, source, target, weight='length')
	_, min_dist_ele_gain, min_dist_keys = find_path_edges(graph, min_dist_path, min_weight='length')
	# Set maximum distance willing to travel
	max_dist = min_dist * percent_shortest_path
	
	# Find total distance and elevation gain of the edges for normalization
	total_dist = 0
	total_ele_gain = 0
	for u, v, data in graph.edges(data=True):
		total_dist += data['length']
		total_ele_gain += data['ele_gain']
	
	# Linear combination: alpha * ele_gain + (1 - alpha) * length
	# Start at 1 to see if min elevation gain is within max distance
	alpha_min = 0.0
	alpha_max = 1.0
	alpha = 1.0
	
	# Dictionary for all paths found within max distance
	paths_found = [{'path': min_dist_path, 'length': min_dist,
					'ele_gain': min_dist_ele_gain, 'keys': min_dist_keys}]
	
	# Binary search for 'iterations' iterations, increasing alpha if path 
	# minimization of the linear combination was within max distance,
	# decreasing alpha if the path was longer than the max distance.
	for _ in range(iterations):
		
		# Create new grades based on binary search of linear combination
		# of normalized distances and elevation gains
		for u, v, k, data in graph.edges(keys=True, data=True):
				graph.add_edge(u, v, key = k, grade = 
							  alpha*data['ele_gain']/total_ele_gain +
							  (1-alpha)*data['length']/total_dist)
		
		# Find shortest path for new grade
		path = nx.shortest_path(graph, source, target, weight='grade')
		path_length, path_ele_gain, path_keys = find_path_edges(graph, path)
		
		############################################
		# Uncomment to view each iteration         #
		#                                          #
		#print(alpha, path_ele_gain, path_length)  #
		#                                          #
		############################################
		
		# If the path found has a shorter distance than the max, 
		if path_length <= max_dist:            
			# Add it to the list of paths to pick from
			paths_found.append({'path': path, 'length': path_length, 
								'ele_gain': path_ele_gain, 'keys': path_keys})
			# Increase alpha min to search higher alphas
			# (weight ele_gain higher in linear combination)
			alpha_min = alpha
			# If the min elevation gain path is within the max distance
			# the best path already found, break out early
			if alpha == 1.0:
				break            
		# If the path found has a longer distance than the max,
		else:
			# Decrease alpha max to search lower alphas
			# (weight length higher in linear combination)
			alpha_max = alpha
		# Set alpha for binary search
		alpha = (alpha_min + alpha_max) / 2
				
	
	# Return the lowest elevation gain within max distance
	best_path = min(paths_found, key=lambda d: d['ele_gain'])
	best_path_dist = best_path['length']
	best_path_gain = best_path['ele_gain']
	best_edge_path = edge_path(best_path['path'], best_path['keys'])
    
	# Show path on actual data model
	# Note: Google Maps and OpenStreetMaps have different data and our UI path
	# may differ from the actual path because of Google Map's intepretation of 
	# the data it recieves.
	ox.plot_graph_route(graph, best_path['path'])
    
	return (best_path_dist, best_path_gain, best_edge_path)


def minimize_elevation_gain_linear(graph, source, target, percent_shortest_path, iterations=10):
	"""
    Minimizes elevation gain within constraint of x% of the shortest path by 
    performing a linear search over alpha(between 1.0 and 0.0) such that each 
    iteration calculates a new weight for every edge as the linear combination
    of alpha * normalized distance + (1 - alpha) * normalized elevation gain, 
    and finds the resulting shortest weighted path. This algorithm samples 
    evenly across alpha interations number of times instead of limiting the 
    search space like the binary search; it is mainly here to compare against 
    the binary method
    
    Parameters:
    -----------
    graph: NetworkX MultiDiGraph
        The graph to perform the search on.
    source: int
        The node id of the source point.
    target: int
        The node id of the target point.
    percent_shortest_path: float (> 1.0)
        The constraint of the maximum distance allowed, represented as a 
        percentage of the shorted distance path (1.0 = 100%).
    iterations: int
        The maximum number of iterations of the linear search to perform, at 
        which point the algorithm will return the best path found thus far. 
        The default here is 10, which was found to be a decent trade-off 
        between runtime and result performance.
        
    Returns: 
    --------
    best_path_dist: float
        The total distance of the best path found
    best_path_gain: float
        The total elevation gain of the best path found
    best_edge_path: list of (int, int, int)
        Each tuple (u, v, key) in the list represents an edge in the graph:
        graph[u][v][key]. The resulting list of edges is the best path found to
        minimize elevation gain given the constraint        
	"""

	# Enforce x% of shortest path 1.0 or larger
	if percent_shortest_path < 1.0:
		raise Exception("Cannot find a path shorter than the shortest path.")
	
	# Find shortest distance path
	min_dist, min_dist_path = nx.single_source_dijkstra(graph, source, target, weight='length')
	_, min_dist_ele_gain, min_dist_keys = find_path_edges(graph, min_dist_path, min_weight='length')
	# Set maximum distance willing to travel
	max_dist = min_dist * percent_shortest_path
	
	# Find total distance and elevation gain of the edges for normalization
	total_dist = 0
	total_ele_gain = 0
	for u, v, data in graph.edges(data=True):
		total_dist += data['length']
		total_ele_gain += data['ele_gain']
	
	# Linear combination: alpha * ele_gain + (1 - alpha) * length
	# Start at 1 to see if min elevation gain is within max distance
	alpha = 1.0
	
	# Dictionary for all paths found within max distance
	paths_found = [{'path': min_dist_path, 'length': min_dist,
					'ele_gain': min_dist_ele_gain, 'keys': min_dist_keys}]
	
	# Linear search for 'iterations' iterations, decreasing alpha with step 
	# size alpha/iterations to evenly sample between 0 and 1. If the path is
	# shorter than the maximum distance, save it, and select the shortest
    # elevation gain among all paths saved
	for _ in range(iterations):
		
		# Create new grades based on binary search of linear combination
		# of normalized distances and elevation gains
		for u, v, k, data in graph.edges(keys=True, data=True):
				graph.add_edge(u, v, key = k, grade = 
							  alpha*data['ele_gain']/total_ele_gain +
							  (1-alpha)*data['length']/total_dist)
		
		# Find shortest path for new grade
		path = nx.shortest_path(graph, source, target, weight='grade')
		path_length, path_ele_gain, path_keys = find_path_edges(graph, path)
		
		############################################
		# Uncomment to view each iteration         #
		#                                          #
		#print(alpha, path_ele_gain, path_length)  #
		#                                          #
		############################################
		
		# If the path found has a shorter distance than the max, 
		if path_length <= max_dist:            
			# Add it to the list of paths to pick from
			paths_found.append({'path': path, 'length': path_length, 
								'ele_gain': path_ele_gain, 'keys': path_keys})
			
			# If the min elevation gain path is within the max distance
			# the best path already found, break out early
			if alpha == 1.0:
				break            
		# linear search over alpha
		alpha = alpha - (alpha / iterations)
				
	
	# Return the lowest elevation gain within max distance
	best_path = min(paths_found, key=lambda d: d['ele_gain'])
	best_path_dist = best_path['length']
	best_path_gain = best_path['ele_gain']
	best_edge_path = edge_path(best_path['path'], best_path['keys'])
    
	return (best_path_dist, best_path_gain, best_edge_path)

	
##############################################################################
# Uncomment to test a single case                                            #
#                                                                            #
#city = nx.read_gpickle('amherst_graph01.gpickle')                           #
#source = #                                                                  #
#target = #                                                                  #
#percent_shortest_path = # Between 1.0 and 2.0                               #
#print(minimize_elevation_gain(city, source, target, percent_shortest_path)) #
#                                                                            #
##############################################################################
