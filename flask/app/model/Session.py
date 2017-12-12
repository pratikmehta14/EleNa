import osmnx.utils as ox
import networkx as nx
from .routing.max_search import maximize
from .routing.min_search import minimize_elevation_gain

class Session_data(object):

    def __init__(self, src_coords, tgt_coords, percent_cutoff):
        self.G = nx.read_gpickle("/Users/pratikm/projects/fall2017/520/EleNa/flask/app/model/amherst_graph01.gpickle")
        self.geometry = nx.get_edge_attributes(self.G,'geometry')
        self.source_coords = src_coords
        self.target_coords = tgt_coords
        self.source = ox.get_nearest_node(self.G,(src_coords[0],src_coords[1]))
        self.target = ox.get_nearest_node(self.G,(tgt_coords[0],tgt_coords[1]))
        self.percent_cutoff = percent_cutoff
        
    def max_elevation_path(self):
        self.max_elevation_path = maximize(self.G,self.source,self.target,self.percent_cutoff)        
        return self.max_elevation_path

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
                mid_y = tgt_y + src_y / 2
                mid_x = tgt_x + src_x / 2
            
            else:
                edge_linestring_coords = self.geometry[edge].coords
                mid_idx = int(len(edge_linestring_coords) / 2) 
                mid_y, mid_x = list(edge_linestring_coords)[mid_idx]
                
            route_coordinates.extend([{'Lat':src_y, 'Long':src_x}, {'Lat':mid_y, 'Long':mid_x}, {'Lat':tgt_y, 'Long':tgt_x}])
        return route_coordinates

