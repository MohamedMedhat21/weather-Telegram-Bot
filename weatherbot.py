import telebot
import weather_botAPIs

API_TOKEN = "your API Token"
bot = telebot.TeleBot(API_TOKEN)
startMsg = "Welcome to Weather Bot!\nwith weather bot you can check current Temperature in a certain location,Also a weather summary is provided\nto start using the bot enter /temp <location> like this\n/temp Cairo"


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, startMsg)


@bot.message_handler(commands=['temp'])
def get_temp(message):
    cityName = message.text[6:]
    # print(cityName)
    temp, summary = weather_botAPIs.getTemp(cityName)
    bot.send_message(message.chat.id,
                     f"current weather in {cityName}\nTemperature: {temp} degree Celsius\nsummary: {summary}")


bot.infinity_polling()
