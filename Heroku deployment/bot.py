import os
from flask import Flask, request
import telebot

import requests
from geopy import Nominatim
import math

API_TOKEN = "your API Token"
bot = telebot.TeleBot(API_TOKEN)
startMsg = "Welcome to Weather Bot!\nwith weather bot you can check current Temperature in a certain location,Also a weather summary is provided\nto start using the bot enter /temp <location> like this\n/temp Cairo"
server = Flask(__name__)


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


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, startMsg)


@bot.message_handler(commands=['temp'])
def get_temp(message):
    cityName = message.text[6:]
    # print(cityName)
    temp, summary = getTemp(cityName)
    bot.send_message(message.chat.id,
                     f"current weather in {cityName}\nTemperature: {temp} degree Celsius\nsummary: {summary}")


@server.route('/' + API_TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://your_heroku_project.com/' + API_TOKEN)
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
