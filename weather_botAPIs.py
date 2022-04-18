import requests
from geopy import Nominatim
import math


def getTemp(cityName):
    geolocator = Nominatim(user_agent="myApp")
    location = geolocator.geocode(cityName)
    # print((location.latitude, location.longitude))

    url = "https://api.ambeedata.com/weather/latest/by-lat-lng"
    querystring = {"lat": location.latitude, "lng": location.longitude}
    headers = {
        'x-api-key': "your API Token",
        'Content-type': "application/json"
    }
    res = requests.request("GET", url, headers=headers, params=querystring).json()

    tmpF = res["data"]["temperature"]
    summary = res["data"]["summary"]

    tmpC = (tmpF - 32) * 5 / 9
    tmpC = math.ceil(tmpC)

    return tmpC, summary
