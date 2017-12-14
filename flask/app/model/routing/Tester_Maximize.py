import max_search
import osmnx as ox, networkx as nx
import googlemaps
from random_path import random_path

def pathGain(graph, path):
    path_ele_gain = 0
    for node in range(len(path) - 1):
        path_ele_gain += graph[path[node]][path[node + 1]][0]['ele_gain']
    return path_ele_gain

if __name__ == '__main__':

    city = nx.read_gpickle('amherst_graph01.gpickle')
    nodes = city.nodes(data=True)


    start = 66592882
    target = 66592890


    pathGenerator = random_path(city, start, target, 1.5, cutoff=15)
    path = pathGenerator.get_randomPath()


    shortest_path = nx.shortest_path(city, start, target, 'length')
    path = max_search.maximize(city, start, target, 1.5)
    print("elevation gain for this path is %d, elevation gain of shortest path is: %d" % (pathGain(city, path), pathGain(city, shortest_path)))

    print('end of tester')
