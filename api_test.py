from __future__ import print_function
import os
from dotenv import load_dotenv
import weatherapi
import time
from weatherapi.rest import ApiException
from pprint import pprint

load_dotenv()
api_key = os.getenv("weather_api_key")
configuration = weatherapi.Configuration()
configuration.api_key['key'] = api_key
api_instance = weatherapi.APIsApi(weatherapi.ApiClient(configuration))



query = input('Enter a region: ')

try:
    # Realtime API
    api_response = api_instance.realtime_weather(query)
    pprint(api_response)
    print(api_response.keys())
    #print(f"Current data is {api_response.localtime}")

except ApiException as e:
    print("Exception when calling APIsApi->realtime_weather: %s\n" % e)