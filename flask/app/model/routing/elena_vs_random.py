from min_search import minimize_elevation_gain
from min_search import minimize_elevation_gain_linear
from max_search import maximize
from random_path import random_path
from random import choice
from Tester_Maximize import pathGain
import matplotlib.pyplot as plt
import inspect, os, sys
sys.path.append( os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) ) )
print ( os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) ) )
from Session import Session_data

def test_run():
	test_session = Session_data()
	print ('cutoff %: ',test_session.percent_cutoff)
	print ('source: ',test_session.source)
	print ('target: ',test_session.target)

	random_path_generator = random_path(test_session.G, test_session.source, test_session.target, test_session.percent_cutoff, 15)
    
	random_route = random_path_generator.get_randomPath()
	random_path_elegain = pathGain(test_session.G,random_route)
	print ("Random path elegain: ", random_path_elegain)

	_, min_path_elegain, __ = test_session.min_elevation_route()
	print ("Min path elegain: ", min_path_elegain)

	_, max_path_elegain, __ = test_session.max_elevation_route()
	print ("Max path elegain: ", max_path_elegain)

	return [min_path_elegain, max_path_elegain, random_path_elegain]

min_elegain_list = []
max_elegain_list = []
rand_elegain_list = []

for i in range(50):
	min_path_elegain, max_path_elegain, random_path_elegain = test_run()
	min_elegain_list.append(min_path_elegain)
	max_elegain_list.append(max_path_elegain)
	rand_elegain_list.append(random_path_elegain)

	
print (min_elegain_list)
print (max_elegain_list)
print (rand_elegain_list)

plt.plot(min_elegain_list,'b-',max_elegain_list,'r-',rand_elegain_list,'g-')
plt.ylabel('elevation gain')
plt.xlabel('Number of tests')
plt.show()
