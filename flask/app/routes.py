from app import app
import googlemaps
from datetime import datetime
import json

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
    	print (maxmin)

    return "Hello, World!"

