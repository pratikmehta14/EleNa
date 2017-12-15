import sys
from app import app
import googlemaps
from datetime import datetime
import json
from flask import render_template, jsonify, request
from osmnx.utils import get_nearest_node
from .model.Session import Session_data

gmaps = googlemaps.Client(key='AIzaSyBNYo6LUPnMZCgCacTyQRZV8oL1_5GJumM')

@app.route('/<request>', methods=['GET'])
def index(request):
	if bool(request):

		request = request.replace("%2C", "," )
		request = request.replace("%20", " " )
		fromm, to, percent, maxmin = request.split(":")

		from_cds = [gmaps.geocode(fromm)[0]['geometry']['location']['lat'], gmaps.geocode(fromm)[0]['geometry']['location']['lng']]
		to_cds = [gmaps.geocode(to)[0]['geometry']['location']['lat'], gmaps.geocode(to)[0]['geometry']['location']['lng']]

		print (from_cds)
		print (to_cds)
		print (percent)
		print (maxmin)

		current_session = Session_data(from_cds,to_cds,float(int(percent)/100))
		
		if maxmin == 'min':
			print ("Minimum elevation route follows these co-ordinates:")
			ele_gain, dist, route = current_session.min_elevation_route()
			route_coords = current_session.route_coordinates(route)
			print (route_coords)
			
		elif maxmin == 'max':
			print ("Maximum elevation route follows these co-ordinates:")
			ele_gain, dist, route = current_session.max_elevation_route()
			route_coords = current_session.route_coordinates(route)
			print (route_coords)

	return jsonify(elevation=ele_gain, distance=dist, waypoints=route_coords)
	#return jsonify([{'Lat': 42.369210, 'Long': -72.500420},{'Lat': 42.369810, 'Long': -72.499116}])

