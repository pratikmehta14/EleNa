# -*- coding: utf-8 -*-
"""
Elevation gain minimization algorithm within x% of shortest path

@author: Jeremy Doyle
"""
import networkx as nx

# Finds the edges used when finding the shortest path for min_weight
# Returning the length, and elevation gain, sum of these edges, and a list of
# keys for each edge.
def find_path_edges(graph, path, min_weight='grade'):
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

# Takes a list of nodes, and a list of keys for each edge,
# returns list of (u, v, key) for each edge
def edge_path(node_path, edge_keys):
	edge_path = []
	for i in range(len(node_path) - 1):
		edge_path.append((node_path[i], node_path[i + 1], edge_keys[i]))
	return edge_path

# Binary search over shortest weight paths where the weight is a linear 
# combination of normalized distances and elevation gains to minimize elevation
# gain within x% of shortest distance path
def minimize_elevation_gain(graph, source, target, percent_shortest_path, iterations=10):
	# Enforce x% of shortest path between 1 and 2
	# TODO
	
	# Find shortest distance path
	min_dist, min_dist_path = nx.single_source_dijkstra(graph, source, target, weight='length')
	_, min_dist_ele_gain, min_dist_keys = find_path_edges(graph, min_dist_path, min_weight='length')
	# Set maximum distance willing to travel
	print (type(min_dist))
	#print (type(max_dist))
	print (type(percent_shortest_path))
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
	############################################################################
	# Uncomment to view path results                                           #
	#                                                                          #
	#print('Max distance:', max_dist, ', Path distance:', best_path['length'], #
	#      ', Path elevation gain:', best_path['ele_gain'])                    #
	#                                                                          #
	############################################################################
	return edge_path(best_path['path'], best_path['keys'])
	
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
