# EleNa
Elevation-based navigation

### By RandomMax:
Bhuvana Surapaneni, Jeremy Doyle, Benjamin Guinsburg, Dilip Chakravarthy Kavarthapu, Pratik Mehta

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
# Using the Application
Download CORS Google Chrome Extension:  
https://chrome.google.com/webstore/detail/allow-control-allow-origi/nlfbmbojpeacfghkpbjhddihlkkiljbi?hl=en

Make sure you have osmnx and googlemaps installed.
flask/app/routes.py has the code to render the HTML.  
To run flask:
```
cd flask
__________________________________________
export FLASK_APP=microblog.py #On OSX
set FLASK_APP=microblog.py    #On Windows
__________________________________________
flask run
```
Open templates/index.html in Google Chrome web browser.

### Using the Interface
![EleNa Interface](EleNa/EleNa.PNG?raw=true "Interface")
