import matplotlib.pyplot as plt
import pandas as pd
import requests

url = "http://cosmicrays.amentum.space"

df = pd.read_csv("experiment.csv", skiprows=1, header=None)

#TODO overwrite the column titles
df.columns = ["time", "dose", "altitude"]

latitude = -33.51 #(S)  [-90, 90] degrees N is +ve
longitude = 147.24 #(E)  [-180, 180] degrees E is +ve
year = '2015'
month = '7'
day = '19'

def get_api_data(particle, api): #This line sets the following formula so we can later change the particle
    url = "http://cosmicrays.amentum.space/" + api + "effective_dose"
    values = [] #This stores the values calulated from the API
    for alt in df['altitude'] :
        #TODO add the altitude to the dictionary
        parameters = {
            "altitude" : alt, #km 
            "latitude" : -33.51, #degrees (N)
            "longitude" : 147.24, #degrees (E)
            "year" : 2015,
            "month" : 7,
            "day" : 19,
            "particle" : particle
            }

        response = requests.get(url, params=parameters) 

        dose_rate = response.json() 

        dose_rate_val = dose_rate['dose rate']['value']

        values.append(dose_rate_val) 
        return values

#create plot of experimental and model predicted doses vs altitude

fig = plt.figure()

axes = fig.add_subplot(111)

axes.semilogy(
    df['time'], df['dose'], 
    label="exp", linestyle="None", marker="+")
#axes.plot(df['altitude'], df['dose'], label="model")

values = get_api_data("gamma", "parma")
axes.semilogy(
    df['time'], values, 
    label="API_g", linestyle="None", marker="+", color="red")

values = get_api_data("total", "parma")
axes.semilogy(
    df['time'], values, 
    label="API_t", linestyle="None", marker="+", color="red")

values = get_api_data("gamma", "cari7")
axes.semilogy(
    df['time'], values, 
    label="API_g", linestyle="None", marker="x", color="blue")

values = get_api_data("total", "cari7")
axes.semilogy(
    df['time'], values, 
    label="API_t", linestyle="None", marker="x", color="blue")

axes.set_xlim(left=0)
axes.set_ylim(bottom=0)
axes.set_xlabel("Time, s")
axes.set_ylabel("Doses, uSv")

plt.legend(loc="lower left")
plt.show()
