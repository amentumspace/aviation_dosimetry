import matplotlib.pyplot as plt
import pandas as pd
import requests

df = pd.read_csv("experiment.csv", skiprows=1, header=None)

df.columns = ["time", "dose", "altitude"]

latitude = -33.51 #(S)  [-90, 90] degrees N is +ve
longitude = 147.24 #(E)  [-180, 180] degrees E is +ve
year = '2015'
month = '7'
day = '19'

def get_api_data(particle, api): 
    url = "http://cosmicrays.amentum.space/" + api + "/ambient_dose"
    values = [] 
    for alt in df['altitude'] :
        
        parameters = {
            "altitude" : alt, #km 
            "latitude" : -33.51, #degrees (N)
            "longitude" : 147.24, #degrees (E)
            "year" : 2015,
            "month" : 7,
            "day" : 19,
            "utc" : 10,
            "particle" : particle
            }
        if particle == "gamma" and api == "cari7":
            parameters["particle"] = "photon"
        response = requests.get(url, params=parameters) 

        dose_rate = response.json() 


        dose_rate_val = dose_rate['dose rate']['value']

        values.append(dose_rate_val) 
    return values


fig = plt.figure()

axes = fig.add_subplot(111)

axes.plot(
    df['time'], df['dose'], 
    label="Experiment", linestyle="None", marker="x")

values = get_api_data("gamma", "parma")
axes.plot(
    df['time'], values, 
    label="PARMA_g", linestyle="None", marker="x", color="red")

values = get_api_data("total", "parma")
axes.plot(
    df['time'], values, 
    label="PARMA_t", linestyle="None", marker="+", color="red")

values = get_api_data("gamma", "cari7")
axes.plot(
    df['time'], values, 
    label="CARI-7_g", linestyle="None", marker="x", color="blue")

values = get_api_data("total", "cari7")
axes.plot(
    df['time'], values, 
    label="CARI-7_t", linestyle="None", marker="+", color="blue")

axes.set_xlim(left=0)
axes.set_ylim(bottom=0)
axes.set_xlabel("Time, s")
axes.set_ylabel("Doses, uSv")

plt.legend(loc="upper left")
#plt.show()

plt.savefig("lineplot.png")