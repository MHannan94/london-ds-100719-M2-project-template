# You don't have to use these classes, but we recommend them as a good place to start!
from dotenv import load_dotenv
import os
import requests
import json
load_dotenv()

class MongoHandler():
    pass

class WeatherGetter():
    def __init__(self):
        # Let's set our secrets and keys from the .env file
        # as environment variables.
        self.BASE_URL = 'https://api.darksky.net'
        self.token = os.getenv('DARKSKY_KEY')
        
        if len(self.token) == 0:
            raise ValueError('Missing API key!')
        
    def get_weather(self, lat, long, date):
        
        year = date[:4]
        month = date[5:7]
        day = date[8:]
        
        url = (self.BASE_URL + '/forecast/' + self.token
               + '/{},{},{}-{}-{}T15:00:00'.format(lat, long, year, month, day)
               + '?units=si&exclude=minutely,hourly,daily,alerts,flags')
        
        resp = requests.get(url).json()
        
        return resp
    
    def get_weather_dates(self, lat, long, dates):
        
        weather_dict = {}
        for date in dates:
            data = self.get_weather(lat, long, date)
            weather_dict[date] = weather_dict.get(date, None)
            weather_dict[date] = data['currently']
        
        return weather_dict
    
    
            