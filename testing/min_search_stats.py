# -*- coding: utf-8 -*-
"""
Generates some statistics to justify our minimization algorithm decisions.
Compares binary search method to equivalant linear method in terms of elevation
gains. Evaluates average run times and elevation gain for different number of
iterations for binary method.  

@author: Jeremy Doyle
"""
import sys
sys.path.append('../flask/app/model/routing')
import random
import min_search
import matplotlib.pyplot as plt
import networkx as nx
from timeit import default_timer as timer

def show_min_search_stats(graph, samples, percent_shortest_path):
    
    equal_shortest_dist = 0.0
    binary_outperform = 0.0
    linear_outperform = 0.0
    mean_shortest_ele_gain = 0.0
    mean_ele_gain_20iter = 0.0
    mean_time_20iter = 0.0
    mean_ele_gain_10iter = 0.0
    mean_time_10iter = 0.0
    mean_ele_gain_5iter = 0.0
    mean_time_5iter = 0.0
    mean_ele_gain_linear = 0.0
    mean_time_linear = 0.0
    
    nodes = [node for node in graph.nodes()]
    
    for _ in range(samples):
        source = random.choice(nodes)
        target = random.choice(nodes)
        # Shortest distance path
        min_dist, min_dist_path = nx.single_source_dijkstra(graph, source, target, weight='length')
        _, min_dist_ele_gain, _ = min_search.find_path_edges(graph, min_dist_path, min_weight='length')
        mean_shortest_ele_gain += min_dist_ele_gain
        
        max_dist = min_dist * percent_shortest_path
        
        # Binary search 5 iterations
        start = timer()
        _, min_5iter_ele_gain, _ = min_search.minimize_elevation_gain(graph, source, target, percent_shortest_path, iterations=5)
        end = timer()
        mean_time_5iter += (end - start)
        mean_ele_gain_5iter += min_5iter_ele_gain
        
        # Binary search 20 iterations
        start = timer()
        _, min_20iter_ele_gain, _ = min_search.minimize_elevation_gain(graph, source, target, percent_shortest_path, iterations=20)
        end = timer()
        mean_time_20iter += (end - start)
        mean_ele_gain_20iter += min_20iter_ele_gain
        
        # Binary search default: 10 iterations
        start = timer()
        min_binary_dist, min_binary_ele_gain, _ = min_search.minimize_elevation_gain(graph, source, target, percent_shortest_path)
        end = timer()
        mean_time_10iter += (end - start)
        mean_ele_gain_10iter += min_binary_ele_gain
        
        # Linear serach default: 10 iterations
        start = timer()
        min_linear_dist, min_linear_ele_gain, _ = min_search.minimize_elevation_gain_linear(graph, source, target, percent_shortest_path)
        end = timer()
        mean_time_linear += (end - start)
        mean_ele_gain_linear += min_binary_ele_gain
        
        # Correctness Tests
        # Should never find a higher elevation gain
        assert(min_binary_ele_gain <= min_dist_ele_gain)
        # Should never exceed max_dist
        assert(min_binary_dist <= max_dist)
        # Cannot be shorter than min_dist
        assert(min_binary_dist >= min_dist)
        
        # Stat trackers
        if min_binary_ele_gain < min_linear_ele_gain:
            binary_outperform += 1
        elif min_binary_ele_gain > min_linear_ele_gain:
            linear_outperform += 1
        
        if min_binary_ele_gain == min_dist_ele_gain:
            equal_shortest_dist += 1
    
    equal_shortest_dist /= samples
    mean_shortest_ele_gain /= samples
    mean_ele_gain_20iter /= samples
    mean_time_20iter /= samples
    mean_ele_gain_10iter /= samples
    mean_time_10iter /= samples
    mean_ele_gain_5iter /= samples
    mean_time_5iter /= samples
    mean_ele_gain_linear /= samples
    mean_time_linear /= samples
    
    # Show how often the shortest distance path is returned as the lowest elevation gain 
    fractions = [equal_shortest_dist, 1 - equal_shortest_dist]
    plt.title('How Often Shortest Path is Minimum Elevation Gain Path (%s samples)' % samples)
    plt.pie(fractions, labels=['shortest path', 'other path'], autopct='%1.1f%%')
    plt.show()
    
    # Show elevation gain between shortest path, and binary method
    fractions = [mean_shortest_ele_gain, mean_ele_gain_10iter]
    plt.title('Elevation Gain Minimization vs Shortest Path (%s samples)' % samples)
    x = (0, 1)
    plt.bar(x, fractions, align='center')
    plt.ylabel('average elevation gain')
    plt.xticks(x, ('Shortest Path', 'Min Algorithm'))
    #plt.pie(fractions, labels=['binary', 'linear', 'tie'], autopct='%1.1f%%')
    plt.show()
    
    # Show Performance of Linear vs Binary methods
    perform = [binary_outperform, linear_outperform, samples - binary_outperform - linear_outperform]
    plt.title('Which Method Returned Lower Elevation Gains (%s samples)' % samples)
    x = (0, 1, 2)
    plt.ylabel('samples')
    plt.bar(x, perform, align='center')
    plt.xticks(x, ('binary', 'linear', 'tie'))
    #plt.pie(fractions, labels=['binary', 'linear', 'tie'], autopct='%1.1f%%')
    plt.show()
    
    # Show elevation gain performance for number of iterations on Binary method
    iters = [5, 10, 20]
    gains = [mean_ele_gain_5iter, mean_ele_gain_10iter, mean_ele_gain_20iter]
    plt.title('Average Elevation Gain of Minimization Algorithm (%s samples)' % samples)
    plt.ylabel('average elevation gain')
    plt.xlabel('number of iterations')
    plt.plot(iters, gains, 'bo-')
    plt.show()
    
    # Show runtime rerformance for number of iterations on Binary method
    runtimes = [mean_time_5iter, mean_time_10iter, mean_time_20iter]
    plt.title('Average Runtime of Minimization Algorithm (%s samples)' % samples)
    plt.ylabel('average runtime (ms)')
    plt.xlabel('number of iterations')
    plt.plot(iters, runtimes, 'bo-')
    plt.show()
    
    print('raw data:', 
          equal_shortest_dist,
          binary_outperform,
          linear_outperform,
          mean_shortest_ele_gain,
          mean_ele_gain_20iter,
          mean_time_20iter,
          mean_ele_gain_10iter,
          mean_time_10iter,
          mean_ele_gain_5iter,
          mean_time_5iter,
          mean_ele_gain_linear,
          mean_time_linear)
        
city = nx.read_gpickle('../flask/app/model/amherst_graph01.gpickle')
show_min_search_stats(city, 1000, 2.0)
