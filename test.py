import requests

url = "http://cosmicrays.amentum.space/api/calculate_dose_rate"

alt = 2.0

parameters = {
    "altitude" : alt, #km 
    "latitude" : 20, #degrees (N)
    "longitude" : 20, #degrees (E)
    "year" : 2015,
    "month" : 7,
    "day" : 19,
    "particle" : "total"
}

response = requests.get(url, params=parameters) #Makes request to the API

dose_rate = response.json() #Pulls out json component, which is converted into our dictionary

dose_rate_val = dose_rate['dose rate']['value'] # Shortcut to what you want in your nested dictionary

values = [] #This is your new list

values.append(dose_rate_val) #.append adds to your list