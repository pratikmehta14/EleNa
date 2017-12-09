
"""
This is the driver class for the program. It has a composition relationship with the
-GUI component
-Algorithm back-end component
-Data model (for algorithm)
"""
import a_star as astar
import flask.app.routes as routes
import model_generator as mg

import webbrowser

class Driver:
    def __init__(self):
        webbrowser.open("templates\index.html")


if __name__ == '__main__':
    driver = Driver()

    #get from_cds, to_cds, percent, and maxmin flag from GUI


    #use model_generator.py to get/modify city graphs
    #create_model_from_city
    gmap_keys = ['AIzaSyBNYo6LUPnMZCgCacTyQRZV8oL1_5GJumM']
    city_name = "Amherst, MA"
    save_file = "amherst_graph01"
    model = mg.create_model_from_city(city_name, save_file, gmap_keys)
