# -*- coding: utf-8 -*-
"""
NetworkX MultiDiGraph examples to help wrap your head around the
dict of dict of dict of dict storage method. Let me know if there is anything 
else I can add to help you understand, of if there are any questions.

@author: Jeremy Doyle
"""

import networkx as nx

run_generic_examples = False
run_example01 = True

if run_generic_examples:
       
    
    """
    Creating a NetworkX MultiDiGraph
    """
    my_graph = nx.MultiDiGraph()
    
    
    
    """
    Reading and Writing NetworkX graphs with gpickle
    """
    # Save a MultiDiGraph using gpickle
    file_path = '../My_Folder/File_Name.gpickle'
    nx.write_gpickle(my_graph, file_path)
    
    # Read pickled networkx graph
    my_graph = nx.read_gpickle(file_path)
    
    
    
    """
    Working with nodes
    """
    # list of nodes
    # [node_id, ... ]
    print(my_graph.nodes())
    
    # list of nodes with attribute dict
    # [(node_id, {attribue: value ... }), ... ]
    print(my_graph.nodes(data=True))
    
    # Example:
    # Iterate over all nodes in the graph
    # node = node id
    # data = dict of {attribute: value}'s
    for node, data in my_graph.nodes(data=True):
        print(node, data)
        # Iterate over all attributes in data
        for attribute in data:
            # attribute name
            print(attribute)
            # attribute value
            print(data[attribute])      
    
    # Get data dict for a single node
    node_id = 0
    data = my_graph.nodes[node_id]
    print(data)
    
    # Get value for an attribute of a single node
    node_id = 0
    attribue = 'attribute'
    attribute_value = my_graph.nodes[node_id][attribute]
    print(attribute_value)
    
    
    
    """
    Working with edges
    """
    # list of all edges in graph
    # Note: With a directed graph there is a seperate edge for
    #       node v to node u, and node u to node v
    # [ (node_id_u, node_id_v), (node_id_v, node_id_u), ... ]
    print(my_graph.edges())
    
    # list of edges with attribute dict
    # [ (node_id_u, node_id_v, {attribute: value, ...}), ... ]
    print(my_graph.edges(data=True))
    
    # list of edges with key and attribute dict
    # Note: With a MultiGraph each node pair u, v can have multiple edges,
    #       each of such edges are referenced by a different key.
    # [ (node_id_u, node_id_v, key, {attribute: value, ...}), ... ]
    print(my_graph.edges(keys=True, data=True))
    
    ############################################################
    # Interacting with my_graph's dict of dict of dict of dict #
    ############################################################
    
    # Getting all nodes connected to node u
    node_id_u = 0
    edges_from_u = my_graph[node_id_u]
    # { node_id_v: edges_between_u_and_v, ... }
    print(edges_from_u)
    
    # Getting all edges from node u to node v
    node_id_u = 0
    node_id_v = 1
    edges_between_u_and_v = my_graph[node_id_u][node_id_v]
    # { key: edge_data, ... }
    print(edges_between_u_and_v)
    
    # Getting data for a single edge from node u to node v with key
    node_id_u = 0
    node_id_v = 1
    key = 0
    edge_data = my_graph[node_id_u][node_id_v][key]
    # { attribute: value, ... }
    print(edge_data)
    
    # Getting an attributes value from a single edge from node u to node v with key
    node_id_u = 0
    node_id_v = 1
    key = 0
    attribute = 'attribute'
    value = my_graph[node_id_u][node_id_v][key][attribute]
    print(value)
    
    # Example:
    # Iterate over all edges in the graph
    for node_id_u, node_id_v, key, data in my_graph.edges(keys=True, data=True):
        uvk_data = my_graph[node_id_u][node_id_v][key]
        #Note: uvk_data and data hold the same information
        print(uvk_data, data)
    

"""
Example 01

We assume you have amherst_graph01.gpickle, and it is in the same
directory as this file.
"""
if run_example01:
    city = nx.read_gpickle('amherst_graph01.gpickle')
    
    ####################################################################
    # Uncomment to view all nodes, and node attributes                 #
    #                                                                  #
    # y: Lattitude of node                                             #
    # x: Longitude of node                                             #
    # osmid: The osmid of the road intersection, which also happens to #
    #        be the node_id. Will consider removing it, seems undeeded.#
    # elevation: Elevation at node in meters.                          #
    # ele_reso: The highest distance (in meters) from which the        #
    #           elevation was interpolated.                            #
    ####################################################################
    #print(city.nodes(data=True))
    
    ####################################################################
    # Uncomment to view all edges u, v, key, and edge attributes       #
    #                                                                  #
    # length: The length in meters of the road.                        #
    # geometry: If the road is not a straight line it has this         #
    #           attribute, and it holds a linestring of all the points #
    #           which make up the road's geometry.                     #
    # ele_gain: The elevation gain in meters along the road.           #
    ####################################################################
    # print(city.edges(data=True))

    
    
    
    
    
    