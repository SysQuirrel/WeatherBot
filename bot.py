from __future__ import print_function
import os
from dotenv import load_dotenv
import weatherapi
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import time
from weatherapi.rest import ApiException
from pprint import pprint

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

api_key = os.getenv("weather_api_key")
configuration = weatherapi.Configuration()
configuration.api_key['key'] = api_key
api_instance = weatherapi.APIsApi(weatherapi.ApiClient(configuration))


@bot.message_handler(commands=["start"])
async def send_welcome_message(message):
    bot.reply_to(message, "I am a bot designed to deliver weather information as well as forecast.")
    
@bot.message_handler(func=lambda m:True)
async def echo_all(message):
    bot.reply_to(message,message.text)
    

try:
    # Realtime API
    api_response = api_instance.realtime_weather(query)
    #pprint(api_response)
    print(f"Current data & time is {api_response["localtime"]['localtime']}")
    

except ApiException as e:
    print("Exception when calling APIsApi->realtime_weather: %s\n" % e)





bot.infinity_polling()

