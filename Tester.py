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

    start = 66592882
    target = 1443766272

    # path = astar.astar_max_distance(city, start, target, 1.5, astar.elevation_heuristic, astar.length_heuristic)
    path = Maximize.maximize(city, start, target, 1.5, astar.elevation_heuristic, astar.length_heuristic)

    print('hi')