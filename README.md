# EleNa
Elevation-based navigation

### By RandomMax:
Bhuvana Surapaneni
Jeremy Doyle
Benjamin Guinsburg
Dilip Chakravarthy Kavarthapu
Pratik Mehta

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
export FLASK_APP=microblog.py
flask run
```
And open templates/index.html in browser.

#****Manually change the assigned directory of self.G in flask/app/model/Session.py****
