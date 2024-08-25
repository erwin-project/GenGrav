import requests
import numpy as np
import pandas as pd
from io import StringIO
from function import GetMessageAPI, GetParamAPI


def GetDataTopex(north, south, west, east):
    # Define the URL where the form is submitted
    url = "https://topex.ucsd.edu/cgi-bin/get_data.cgi"

    # Define the form data
    grav_data = dict(north=north, south=south, west=west, east=east, mag=0.1)
    topo_data = dict(north=north, south=south, west=west, east=east, mag=1)

    # Send the POST request with form data
    response_grav = requests.post(url, data=grav_data)
    response_topo = requests.post(url, data=topo_data)

    # Check if the request was successful
    if response_grav.status_code == 200 and response_topo.status_code == 200:
        # Process the returned data
        grav_dataset = pd.read_csv(StringIO(response_grav.text),
                                   sep=r'\s+',
                                   on_bad_lines='skip',
                                   names=['easting', 'northing', 'grav_value'],
                                   header=None)
        topo_dataset = pd.read_csv(StringIO(response_topo.text),
                                   sep=r'\s+',
                                   on_bad_lines='skip',
                                   names=['easting', 'northing', 'topo_value'],
                                   header=None)

        topex_dataset = pd.merge(grav_dataset, topo_dataset, on=['easting', 'northing'])

        return grav_dataset, topo_dataset, topex_dataset

    else:
        print(f"Failed to retrieve data")

        return None, None, None


