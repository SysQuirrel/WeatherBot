from __future__ import print_function
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os
import asyncio
import logging
from dotenv import load_dotenv
import weatherapi
from weatherapi.rest import ApiException

# Getting all the api keys and tokens from the .env file
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
api_key = os.getenv("weather_api_key")

# Configuring weatherapi application
configuration = weatherapi.Configuration()
configuration.api_key["key"] = api_key
api_instance = weatherapi.APIsApi(weatherapi.ApiClient(configuration=configuration))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("bot.log"),  # save logs to bot.log
        logging.StreamHandler()  # also print to console
    ]
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hi! Please enter the name of a city to get the weather:",
        reply_markup=ReplyKeyboardRemove(),
    )

async def handle_weather_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    query = update.message.text
    
    logger.info("User %s asked for weather in: %s", user.first_name, query)
    
    try:
        # Realtime Weather API call
        api_response = api_instance.realtime_weather(query)
     
        localtime = api_response["location"]["localtime"]
        last_updated = api_response["current"]["last_updated"]
        condition_icon = api_response["current"]["condition"]["icon"]
        
        temp_c = api_response["current"]["temp_c"]
        feels_like_c = api_response["current"]["feelslike_c"]
        humidity = api_response["current"]["humidity"]
        
        location_name = api_response["location"]["name"]
        latitude = api_response["location"]["lat"]
        longitude = api_response["location"]["lon"]

        caption = (
            f"Local time: {localtime}\n"
            f"Last updated at {last_updated}\n"
            f"Weather in {location_name} ({latitude}, {longitude})\n"
            f"Temperature: {temp_c}°C\n"
            f"Feels like {feels_like_c}°C\n"
            f"Humidity {humidity}"
        )
        if condition_icon:
            # Fix the icon URL by adding https: protocol
            if condition_icon.startswith('//'):
                condition_icon = f"https:{condition_icon}"
            
            logger.info("Using icon URL: %s", condition_icon)
            
            try:
                await update.message.reply_photo(
                    photo=condition_icon,
                    caption=caption,
                    parse_mode='Markdown'
                )
                logger.info("Successfully sent weather photo")
            except Exception as photo_error:
                logger.error("Failed to send photo: %s", photo_error)
                # Fallback to text-only message
                await update.message.reply_text(
                    caption,
                    parse_mode='Markdown'
                )
        else:
            # No icon available, send text only
            await update.message.reply_text(
                caption,
                parse_mode='Markdown'
            )
        
    except ApiException as e:
        await update.message.reply_text("Sorry, I couldn't fetch the weather. Please check the city name.")
        logger.error("Exception when calling API: %s", e)
    except Exception as e:
        await update.message.reply_text("Sorry, an unexpected error occurred.")
        logger.error("Unexpected error: %s", e)

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    
    # Add handler for text messages (city names)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_weather_request))
    
    logger.info("Bot starting...")
    app.run_polling()