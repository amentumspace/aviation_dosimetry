import matplotlib.pyplot as plt
import pandas as pd
from pint import UnitRegistry
import numpy as np
import requests

df = pd.read_csv("flight_data.csv")

url = "http://cosmicrays.amentum.space/cari7/effective_dose"

df.columns = [
    "altitude",
    "lat",
    "long",
    "hawka",
    "hawka_er",
    "hawki",
    "hawki_er",
    "liu",
    "liu_er",
    "tepc",
    "tepc_er",
    "ami",
    "siev",
    "siev_er",
    "epc"
    ]

row1 = df.iloc[0]

values = []

for index, row in df.iterrows():
    alt =  2 #df["altitude"]
    lat = row["lat"]
    lon = row["long"]

    parameters = {
        "altitude" : alt, #km 
        "latitude" : lat, #degrees (N)
        "longitude" : lon, #degrees (E)
        "year" : 2003,
        "month" : 5,
        "day" : 6,
        "utc" : 12,
        "particle" : "total"
    }
    response = requests.get(url, params=parameters) 

    dose_rate = response.json() 

    dose_rate_val = dose_rate['dose rate']['value']

    values.append(dose_rate_val) 




row1["hawka"]
row1["liu"]
row1["tepc"]
row1["epc"]
