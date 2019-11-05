# You don't have to use these classes, but we recommend them as a good place to start!
from dotenv import load_dotenv
import os
import requests
import json
import pymongo
load_dotenv()

class MongoHandler():
    def __init__(self, db):
        self.client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
        self.db = self.client[db]
    
    def add_docs(self, coll, recs):
        # for each record in my list of records
        for rec in recs:
            # check for any games played in rain
            if rec['Games in rain'] != 0:
                data = {'name':rec['name'],
                        'goals':rec['Total goals'],
                        'wins': rec['Num wins'],
                        'win percentage in rain': rec['Wins in rain percentage']} # this will only be included if any games were
                                                                                  # played in rain
            else:
                data = {'name':rec['name'],
                        'goals':rec['Total goals'],
                        'wins': rec['Num wins']}
            result = self.db[coll].insert_one(data)
            print(result) # to confirm the document was written
    # function just to query the collection (see if its populated)
    def all_docs(self, coll):
        query = self.db[coll].find({})
        for q in query:
            print(q)
    # option to empty the collection before populating
    def empty_coll(self, coll):
        result = self.db[coll].delete_many({})
        print(result)

class WeatherGetter():
    def __init__(self):
        # Let's set our secrets and keys from the .env file
        # as environment variables.
        self.BASE_URL = 'https://api.darksky.net'
        self.token = os.getenv('DARKSKY_KEY')
        
        if len(self.token) == 0:
            raise ValueError('Missing API key!')
        
    def get_weather(self, lat, long, date):
        # split the date into components
        year = date[:4]
        month = date[5:7]
        day = date[8:]
        
        url = (self.BASE_URL + '/forecast/' + self.token
               + '/{},{},{}-{}-{}T15:00:00'.format(lat, long, year, month, day)
               + '?units=si&exclude=minutely,hourly,daily,alerts,flags')
        
        resp = requests.get(url).json()
        
        return resp
    # create a dictionary of weather data for the selected dates
    def get_weather_dates(self, lat, long, dates):
        
        weather_dict = {}
        for date in dates:
            data = self.get_weather(lat, long, date)
            weather_dict[date] = weather_dict.get(date, None)
            weather_dict[date] = data['currently']
        
        return weather_dict
    
    
            