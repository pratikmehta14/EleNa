import networkx as nx
import numpy as np
import copy
import random

class random_path:

    def __init__(self, graph, source, target, percent_shortest_path, cutoff):
        self.random_paths = []
        self.graph = graph
        self.percent_shortest_path = percent_shortest_path
        self.shortest_path = nx.shortest_path(self.graph, source, target, 'length')
        self.max_length = nx.shortest_path_length(graph, source, target, 'length') * self.percent_shortest_path
        self.build_random_paths(cutoff)

    def build_random_paths(self, cutoff):
        graph = self.graph

        shortest_path = self.shortest_path
        random_paths = []

        for i in range(len(shortest_path)-1):
            #every 10th, or last
            if (i % 10 == 0 or i == len(shortest_path)-1):
                graph_truncated = copy.deepcopy(graph)
                trunc1 = shortest_path[0:i]
                trunc2 = shortest_path[i + 2:]
                graph_truncated.remove_nodes_from(trunc1 + trunc2)

                currentNode = shortest_path[i]
                nextNode = shortest_path[i + 1]

                interPaths = nx.all_simple_paths(graph_truncated, currentNode, nextNode, cutoff=cutoff)
                random_paths.append(list(interPaths))
            else:
                random_paths.append([])

        self.random_paths = random_paths


    def get_randomPath(self):
        if (len(self.random_paths) == 0): print("You must call the randomPath function first!")

        working_path = copy.deepcopy(self.shortest_path)
        for i in range(len(self.shortest_path)-1):
            if (i % 10 == 0 or i == len(self.shortest_path) - 1):
                paths = list(self.random_paths[i])
                # random_path = paths[np.random.randint(0, len(paths)-1)]
                random_path = random.choice(paths)

                node1 = self.shortest_path[i]
                node2 = self.shortest_path[i + 1]
                node1_ind = working_path.index(node1)
                node2_ind = working_path.index(node2)

                x = working_path[0:node1_ind]
                y = working_path[node2_ind+1:]
                path = (x + random_path + y)

                if (self.pathLength(self.graph, path) < self.max_length):
                    working_path = path

        return working_path



    def pathLength(self, graph, path):
        path_length = 0
        for node in range(len(path) - 1):
            path_length += graph[path[node]][path[node + 1]][0]['length']
        return path_length



