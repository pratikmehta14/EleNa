import a_star as astar

import Maximize
import model_generator as mg
import osmnx as ox, networkx as nx
import googlemaps

if __name__ == '__main__':
    # gmap_keys = ['AIzaSyBNYo6LUPnMZCgCacTyQRZV8oL1_5GJumM']
    # city_name = "Amherst, MA"
    # save_file = "amherst_graph01"
    # graph = mg.create_model_from_city(city_name, save_file, gmap_keys)

    city = nx.read_gpickle('amherst_graph01.gpickle')
    nodes = city.nodes(data=True)

    edges = city.edges(data=True)

    start = 66592882

    target_minus_5 = 66715367
    target_minus_1 = 66704462
    target = 66592890

    simple_paths = list(nx.all_simple_paths(city, target_minus_5, target, cutoff=10))


    # path = astar.astar_max_distance(city, start, target, 1.5, astar.elevation_heuristic, astar.length_heuristic)
    path = Maximize.maximize(city, start, target, 1.5, astar.elevation_heuristic, astar.length_heuristic)

    print('hi')