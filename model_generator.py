# -*- coding: utf-8 -*-
"""
Functions used to create, modify, and save networkx multidigraphs used to model
a city to perform elevation based navigation on.

@author: Jeremy Doyle
"""
import osmnx as ox, networkx as nx
import googlemaps
from timeit import default_timer as timer



def create_model_from_city(city_name, save_file, high_res=True, max_calls_per_key=2250, gmap_keys):
    # Calculate total number of api calls usable
    api_calls_left = len(gmap_keys) * max_calls_per_key
    # Create networkx mutlidigraph of city
    city_graph = osmnx_graph_from_place(city_name)
    # Filter out irrelavent edge information
    filter_edge_attributes(city_graph, ['length', 'geometry'])
    # Set up Google Maps clients for each api key
    gmap_clients = [googlemaps.Client(key=k) for k in gmap_keys]
    # Add elevation data to city model
    add_elevation_data(city_graph, gmap_clients, api_calls_left, max_calls_per_key, high_res)
    # Save city model
    pickle(city_graph, save_file)
    # Return city graph
    return city_graph
    
    

def osmnx_graph_from_place(city_name):
    print("Initializing Graph of {} with OSMnx...".format(city_name))
    start = timer()
    
    city_graph = ox.graph_from_place(city_name, network_type='walk')
    
    end = timer()
    print("Time: {}".format(end - start))
    return city_graph



def filter_edge_attributes(graph, attributes_to_keep):
    print("Removing all edge attributes from {} besides {}...".format(graph, attributes_to_keep))
    start = timer()
    
    for u, v, k, data in graph.edges(keys=True, data=True):
        attributes_to_del = []
        for attribute in graph[u][v][k]:
            if not attribute in attributes_to_keep:
                attributes_to_del += [attribute]
        for attribute in attributes_to_del:
            del graph[u][v][k][attribute]
    # return graph with deleted edges.
    return graph
            
    end = timer()
    print("Time: {}".format(end - start))
    


def add_node_elevation_data(graph, gmap_clients, api_calls_left, max_calls_per_key, max_nodes_per_call=350):
    print("Adding node elevation data from Google Maps Elevation API...")
    start = timer()
    
    # Get all yxs for every node in graph
    yx_list = [(data['y'], data['x']) for node, data in graph.nodes(data=True)]
    # Break up list into lists of at most max_nodes_per_call nodes
    yx_lists = [yx_list[i:i + max_nodes_per_call] for i in range(0, len(yx_list), max_nodes_per_call)]
   
    # Create and populate list of elevation lists by calling google maps api for each
    # sublist of at most max_nodes_per_call
    elevation_lists = []
    for yxs in yx_lists:
        # For each sublist call googlemaps api and append list of elevation data
        gmap_client = gmap_clients[(api_calls_left - 1) // max_calls_per_key]
        elevation_data = gmap_client.elevation(yxs)
        elevation_lists.append(elevation_data)
        api_calls_left -= 1
    # Condense lists of elevation data to single list
    all_ele_data = [ele_data for sublist in elevation_lists for ele_data in sublist]
    
    # Extract elevations for each node and assign to node attribute
    elevations = [ele_data['elevation'] for ele_data in all_ele_data]
    nx.set_node_attributes(graph, name='elevation', values=dict(zip(graph.nodes(), elevations)))
    
    # Extract elevation resolutions for each node and assign to node attribute
    # Note: this will be used to determine how many samples to use between nodes
    resolutions = [ele_data['resolution'] for ele_data in all_ele_data]
    nx.set_node_attributes(graph, name='ele_reso', values=dict(zip(graph.nodes(), resolutions)))
    
    end = timer()
    print("Time: {}".format(end - start))
    
    #return api calls left after all calls
    return api_calls_left
    


def add_elevation_data(graph, gmap_clients, api_calls_left, max_calls_per_key, high_res):
    print("Adding elevation data to graph from Google Maps Elevation API...")
    start = timer()
    # Add elevation data at each node, and update api_calls_left
    api_calls_left = add_node_elevation_data(graph, gmap_clients, api_calls_left, max_calls_per_key)
    
    # Add elevation gains for every edge in the graph
    for u, v, k, data in graph.edges(keys=True, data=True):
        expected_reso = min(graph.nodes[u]['ele_reso'], graph.nodes[v]['ele_reso'])
        sample_reso = int(2 + data['length'] // expected_reso)
        # If elevation gain has not been added for this edge yet, add it
        if not 'ele_gain' in data:
            # Call api to get elevations for edge if we want higher resolition than
            # elevation at each node, there are api calls left, and if the desired sample
            # resolution is more than just the two nodes.
            if high_res and api_calls_left > 0 and sample_reso > 2:
                gmap_client = gmap_clients[(api_calls_left - 1) // max_calls_per_key]
                # Get elevation data for edge                 
                if 'geometry' in data:
                    # If the edge has a geometry attribute (not a straight line), get
                    # the list of line segments.
                    xs, ys = data['geometry'].xy
                    yx_list = list(zip(ys, xs))
                else:
                    # Otherwise, the edge is a straight line.
                    u_y = graph.nodes[u]['y']
                    u_x = graph.nodes[u]['x']
                    v_y = graph.nodes[v]['y']
                    v_x = graph.nodes[v]['x']
                    yx_list = [(u_y, u_x), (v_y, v_x)]
                # Request elevation data along road, with number of samples = sample_reso
                elevations_data = gmap_client.elevation_along_path(yx_list, sample_reso)
                api_calls_left -= 1
                # Extract just the elevations at each sample and store it in a list
                elevation_samples = [e['elevation'] for e in elevations_data]
                
            # Otherwise, we can get a lower resolution of elevation gain between two
            # nodes by just using the elevation at each node.
            else:
                elevation_samples = [graph.nodes[u]['elevation'], graph.nodes[v]['elevation']]
            
            # Use elevation_samples to add elevation gain to edge by summing gains from
            # u to v over the samples
            gain = sum_ele_gains(elevation_samples)
            graph.add_edge(u, v, key = k, ele_gain = gain)
            
            # We can add the elevation gain for v to u by summing the gains backwards
            # Note: if both nodes are the same, [u][v][k] = [v][u][k], and instead the
            # key differentiates the forward and backward edge. For this case we just
            # make a second api call instead.
            if u != v:
                gain = sum_ele_gains(elevation_samples, backwards=True)
                graph.add_edge(v, u, key = k, ele_gain = gain)
        
    end = timer()
    print("Time: {}".format(end - start))
    return api_calls_left



def sum_ele_gains(elevation_list, backwards=False):
    # Reverse list if backwards is true
    if backwards:
        elevation_list = elevation_list[::-1]
    # For each elevation in list, sum the gain between current and last elevation
    cur_ele = elevation_list[0]
    gain = 0
    for ele in elevation_list:
        last_ele = cur_ele
        cur_ele = ele
        gain += max(0, cur_ele - last_ele) # Discard elevation loss            
    return gain



def pickle(graph, save_file):
    print("Saving to file location {}.gpickle...".format(save_file))
    start = timer()
    nx.write_gpickle(graph, save_file + '.gpickle')
    end = timer()
    print("Time: {}".format(end - start))













    