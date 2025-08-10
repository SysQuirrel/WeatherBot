import os
import telebot
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=["start"])
def send_welcome_message(message):
    bot.reply_to(message, "I am a bot designed to deliver weather information as well as forecast.")
    
@bot.message_handler(func=lambda m:True)
def echo_all(message):
    bot.reply_to(message,message.text)
    







bot.infinity_polling()

