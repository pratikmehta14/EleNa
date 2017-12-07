# EleNa
Elevation-based navigation

### Installing OSMnx
with pip:
```
pip install osmnx
```
Note: If you are pip installing OSMnx, install geopandas and rtree first. It's easiest to use conda-forge to get these dependencies installed.

with conda:
```
conda install -c conda-forge osmnx
```

### Installing google-maps-services-python
```
pip install -U googlemaps
```
### GUI
flask/app/routes.py has the code to render the HTML.
To run flask:
```
cd flask
flask run
```
And open templates/index.html in browser.
