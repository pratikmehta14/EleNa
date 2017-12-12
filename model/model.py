import osmnx.utils as ox
import networkx as nx
from routing.max_search import maximize
from routing.min_search import minimize_elevation_gain

class Session_data(object):
    G = nx.read_gpickle("/Users/pratikm/projects/fall2017/520/EleNa/model/amherst_graph01.gpickle") 
    geometry = nx.get_edge_attributes(G,'geometry')

    def __init__(self, src_coords, tgt_coords, percent_cutoff):
        self.source_coords = src_coords
        self.target_coords = tgt_coords
        self.source = ox.get_nearest_node(G,src_coords[0],src_coords[1])
        self.target = ox.get_nearest_node(G,tgt_coords[0],tgt_coords[1])
        self.percent_cutoff = percent_cutoff
        
    def max_elevation_path():
        self.max_elevation_path = maximize(G,self.source,self.target,self.percent_cutoff)        
        return self.max_elevation_path

    def min_elevation_route():
        self.min_elevation_route = minimize_elevation_gain(G,self.source,self.target,self.percent_cutoff)
        return self.min_elevation_route

    def route_coordinates(route):
        route_coordinates = []
        for edge in route:
            src, tgt, edge_id = edge
            edge_data = graph[src][tgt][edge_id]
            
            src_y, src_x = graph[src].y, graph[src].x
            tgt_y, tgt_x = graph[tgt].y, graph[src].x

            if 'geometry' not in edge_data:
                mid_y = tgt_y + src_y / 2
                mid_x = tgt_x + src_x / 2
            
            else:
                edge_linestring_coords = geometry[edge].coords
                mid_idx = len(edge_linestring_coords) / 2 
                mid_y, mid_x = list(edge_linestring_coords)[mid_idx]
                
            route_coordinates.extend([{'Lat':src_y, 'Long':src_x}, {'Lat':mid_y, 'Long':mid_x}, {'Lat':tgt_y, 'Long':tgt_x}])
        return route_coordinates



