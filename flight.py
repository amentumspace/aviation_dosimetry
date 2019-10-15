import matplotlib.pyplot as plt
import pandas as pd
from pint import UnitRegistry
import numpy as np
import requests

ureg = UnitRegistry()
df = pd.read_csv("flight_data.csv")


df.columns = [
    "altitude",
    "lat",
    "long",
    "hawka",
    "hawkaerr",
    "hawki",
    "hawkierr",
    "liu",
    "liuerr",
    "tepc",
    "tepcerr",
    "ami",
    "siev",
    "sieverr",
    "epc"
    ]

for model in ["parma", "cari7"]:
    url = "http://cosmicrays.amentum.space/" + model + "/effective_dose"
    values = []

    for index, row in df.iterrows():
        alt = row["altitude"] * ureg.foot
        alt = alt.to(ureg.kilometer).magnitude
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

    df[model] = values



labels = ['G1', 'G2', 'G3', 'G4', 'G5', 'G6']

x = np.arange(df.shape[0])

width = 0.1  # the width of the bars

fig, ax = plt.subplots()

rects1 = ax.bar(x - width * 2.5, df["hawka"], width, label='HAWKarcs', yerr=df["hawkaerr"])
rects1 = ax.bar(x - width * 1.5, df["liu"], width, label='Liulin', yerr=df["liuerr"])
rects2 = ax.bar(x - width/2, df["tepc"], width, label='TEPC', yerr=df["tepcerr"])
rects3 = ax.bar(x + width/2, df["epc"], width, label='EPCARD')
rects3 = ax.bar(x + width * 1.5, df["cari7"], width, label='CARI-7')
rects3 = ax.bar(x + width * 2.5, df["parma"], width, label='PARMA')


ax.set_ylabel('Ambient dose equivalent, uSv/hr')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()

#plt.show()

plt.savefig("barplot.png")