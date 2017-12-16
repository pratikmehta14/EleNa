"""
Graph data, routing APIs, and route formatting for GUI

@author: Pratik Mehta
"""

import osmnx.utils as ox
import networkx as nx
from routing.max_search import maximize
from routing.min_search import minimize_elevation_gain
import inspect, os
from random import choice, uniform

class Session_data(object):

    def __init__(self, src_coords=None, tgt_coords=None, percent_cutoff=None):
        self.G = nx.read_gpickle(os.path.dirname(os.path.abspath(inspect.stack()[0][1])) + "/amherst_graph01.gpickle")
        self.geometry = nx.get_edge_attributes(self.G,'geometry')

        if src_coords == None and tgt_coords == None:
            self.source, self.target = self.random_disconnected_node_pair()
        else:
            self.source_coords = src_coords
            self.target_coords = tgt_coords
            self.source = ox.get_nearest_node(self.G,(src_coords[0],src_coords[1]))
            self.target = ox.get_nearest_node(self.G,(tgt_coords[0],tgt_coords[1]))
        
        if percent_cutoff == None:
            self.percent_cutoff = uniform(100,200) / 100
        else:
            self.percent_cutoff = percent_cutoff
        
    def max_elevation_route(self):
        self.max_elevation_route = maximize(self.G,self.source,self.target,self.percent_cutoff)        
        return self.max_elevation_route

    def min_elevation_route(self):
        print(type(self.percent_cutoff))
        self.min_elevation_route = minimize_elevation_gain(self.G,self.source,self.target,self.percent_cutoff)
        return self.min_elevation_route

    def route_coordinates(self,route):
        route_coordinates = []
        for edge in route:
            src, tgt, edge_id = edge
            edge_data = self.G[src][tgt][edge_id]
            
            src_y, src_x = self.G.nodes[src]['y'], self.G.nodes[src]['x']
            tgt_y, tgt_x = self.G.nodes[tgt]['y'], self.G.nodes[tgt]['x']

            if 'geometry' not in edge_data:
                mid_y = (tgt_y + src_y) / 2
                mid_x = (tgt_x + src_x) / 2
            
            else:
                edge_linestring_coords = self.geometry[edge].coords
                mid_idx = int(len(edge_linestring_coords) / 2) 
                mid_x, mid_y = list(edge_linestring_coords)[mid_idx]
                
            route_coordinates.extend([{'Lat':src_y, 'Long':src_x}, {'Lat':mid_y, 'Long':mid_x}, {'Lat':tgt_y, 'Long':tgt_x}])

        route_cds = []

        if (len(route_coordinates)>23):
            ll = int (len(route_coordinates)/23 + 1)
            i = 0
            while (i<len(route_coordinates)):
                route_cds.extend([{'Lat':route_coordinates[i]['Lat'], 'Long':route_coordinates[i]['Long']}])
                i = i+ll

        #route_cds = route_cds[2:-2]

        return route_cds

    def random_disconnected_node_pair(self):
        src = choice(list(self.G.nodes()))
        while(True):
            tgt_set = set(self.G.nodes())
            tgt_set.difference_update(list(self.G.neighbors(src)) + [src])
            tgt = choice(list(tgt_set))
            min_hops = nx.shortest_path_length(self.G, source=src, target=tgt)
            if min_hops < 40:
                print ("min hops between src and tgt: ",min_hops)
                break
        return [src, tgt]

