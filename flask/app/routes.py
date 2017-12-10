from app import app
import googlemaps
from datetime import datetime
import json
from flask import render_template, jsonify, request

gmaps = googlemaps.Client(key='AIzaSyBNYo6LUPnMZCgCacTyQRZV8oL1_5GJumM')

@app.route('/<request>', methods=['GET'])
def index(request):
    if bool(request):

    	request = request.replace("%2C", "," )
    	request = request.replace("%20", " " )
    	fromm, to, percent, maxmin = request.split(":")

    	if (maxmin == 'max'):
    		maxmin = 1
    	elif (maxmin == 'min'):
    		maxmin = 0

    	from_cds = [gmaps.geocode(fromm)[0]['geometry']['location']['lat'], gmaps.geocode(fromm)[0]['geometry']['location']['lng']]
    	to_cds = [gmaps.geocode(to)[0]['geometry']['location']['lat'], gmaps.geocode(to)[0]['geometry']['location']['lng']]

    	print (from_cds)
    	print (to_cds)
    	print (percent)
    	data = {'username': 'Pang', 'site': 'stackoverflow.com'}

        

        

    return jsonify([{'Lat': 42.369210, 'Long': -72.500420},{'Lat': 42.369810, 'Long': -72.499116}])

