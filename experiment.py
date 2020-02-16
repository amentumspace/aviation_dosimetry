from datetime import datetime
from datetime import timedelta
import matplotlib.pyplot as plt
import numpy as np 
import os
import pandas as pd
import pytz
import requests

df = pd.read_csv("experiment.csv", skiprows=1, header=None)
df.columns = ["time", "dose", "altitude"]

# West Wyalong NSW Australia
latitude = -33.98 #(S)  [-90, 90] degrees N is +ve
longitude = 147.3 #(E)  [-180, 180] degrees E is +ve

# create a datetime object with launch start time 09:15 AEST 19th July 2019
dt = datetime(2015,7,19, 9, 15, tzinfo=pytz.timezone('Australia/Sydney'))      
# convert to Universal coordinated time (UTC)
dt = dt.astimezone(pytz.utc)      
# new column with UTC time of each measurement
df['datetime'] = df['time'].apply(lambda x : timedelta(seconds=x) + dt)
# set the time as the index to make plotting simpler
df.set_index('time', inplace=True)   
# convert to decimal hours for plotting
df.index /= 3600

def get_api_data(row, particle, api):
    """
    Make an API call for selected API and particle

    Args: row of pandas dataframe, name of api, name of particle

    """ 
    # check env variable to over-ride 
    url = "http://cosmicrays.amentum.space/" 

    if os.environ.get('URL') is not None:
         url = os.environ.get('URL')

    url += api 
    url += "/ambient_dose"
    
    parameters = {
        "altitude" : row.altitude, #km 
        "latitude" : latitude, #degrees (N)
        "longitude" : longitude, #degrees (E)
        "year" : row.datetime.year, # access using datetime object in row index
        "month" : row.datetime.month,
        "day" : row.datetime.day,
        "utc" : row.datetime.hour, 
        "particle" : particle
    }

    # account for different naming convention in cari7 api
    if particle == "gamma" and api == "cari7":
        parameters["particle"] = "photon"
    
    # make the call and handle errors
    try:
        response = requests.get(url, params=parameters) 
        response.raise_for_status()
    except requests.exceptions.HTTPError as e: 
        print("HTTP error", e)
    except requests.exceptions.RequestException as e: 
        print("Request error", e)

    # retrieve and return the dose rate
    dose_rate = response.json() 
    dose_rate_val = dose_rate['dose rate']['value']
    return dose_rate_val

# Create new columns by calling API endpoints for gammas and total ambient dose equivalents
df['parma gamma'] = df.apply(get_api_data, args=("gamma", "parma"), axis=1)
df['parma total'] = df.apply(get_api_data, args=("total", "parma"), axis=1)
df['cari7 gamma'] = df.apply(get_api_data, args=("gamma", "cari7"), axis=1)
df['cari7 total'] = df.apply(get_api_data, args=("total", "cari7"), axis=1)

for plot_total in [True, False]:
    # create a plot of just gamma dose, another with total doses on log y plot

    fig = plt.figure()
    axes = fig.add_subplot(111)
    
    df['dose'].plot(
        label="Experiment", linestyle="-", drawstyle="steps-post", 
        color="Black", logy=plot_total)
    df['parma gamma'].plot(
        label="PARMA", linestyle="None", marker="s", 
        color="DodgerBlue", logy=plot_total)
    df['cari7 gamma'].plot(
        label="CARI7", linestyle="None", marker="o", 
        color="OrangeRed", logy=plot_total)
    
    # only plot totals on second graph
    if plot_total: 
        df['parma total'].plot(
            label="PARMA total", linestyle="None", marker="s", 
            fillstyle='none', color="DodgerBlue", logy=True)
        df['cari7 total'].plot(
            label="CARI7 total", linestyle="None", marker="o", 
            fillstyle='none',  color="OrangeRed", logy=True)

    axes.set_xlim(left=0)
    axes.set_ylim(bottom=0)
    axes.set_xlabel("Duration, hr")
    axes.set_ylabel("Ambient Dose Equivalent (gamma), uSv/hr")

    plt.legend(loc="upper left")

    ax2 = axes.twinx()
    ax2.set_ylim(bottom=0, top=df.altitude.max()*1.2)
    df.altitude.plot(linestyle=":", logy=plot_total, color="Grey")
    ax2.set_ylabel("Altitude, km")

    filename = "lineplot"
    if plot_total : filename += "_totals"
    plt.savefig(filename+".png")


