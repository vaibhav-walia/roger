import sys
import googlemaps
import pyowm
import pandas as pd
import numpy as np
from time import sleep

OWM_API_KEY = sys.argv[1] #weather api key should be passed as first argument
MAP_API_KEY = sys.argv[2] #gmap api key should be passed as second argument

owm = pyowm.OWM(OWM_API_KEY)
gmaps = googlemaps.Client(key=MAP_API_KEY)
stops = pd.DataFrame()

'''Returns a dictionary containing current latitute and longitutde'''
def getLocation():
    return (gmaps.geolocate())['location'];

'''Calls the weather api to get weather at a particular latitute and
longitutde '''
def getWeather(lat,lng):
    obs = owm.weather_at_coords(lat,lng)
    #print(lat,',',lng,':',obs.get_weather().get_status())
    return obs.get_weather().get_status()

'''Reads the stop info from stops.txt'''
def getStopInfo():
    global stops
    stops = pd.read_csv('stops.txt',index_col='stop_code')

'''Given a stop, returns the weater status at that stop'''
def getWeatherAtStop(stopCode):
    #read stop data only once
    if stops.empty:
        getStopInfo()
    #validate stop code
    if stopCode not in stops.index:
        return 'Invalid stop code'

    stop = stops.loc[stopCode]
    lat = stop['stop_lat']
    lng = stop['stop_lon']
    sleep(1.1)
    weather = getWeather(float(lat),float(lng))
    print(lat,lng,weather)
    return weather

def getWeatherAtAllStops():
    print('working...')
    getStopInfo()
    '''get weather for all stops, write to file after every 500'''
    numLoops = 7000//500

    for i in  range(4,numLoops+1):
        print('starting ',i)
        filename = 'weather'+str(i)+'.csv'
        end = i*500
        start = end-500
        # print(start,end,'weather'+str(i)+'.csv')
        weather = [getWeatherAtStop(index) for index, stop in stops[start:end].iterrows()]
        stopsT = stops[start:end].copy()
        stopsT['weather'] = weather
        stopsT.to_csv(filename)
        print(i,' done')

    getRemainingStops()

def getRemainingStops():
    print('starting ',15)
    filename = 'weather'+str(15)+'.csv'
    end = 7049
    start = 7000
    # print(start,end,'weather'+str(i)+'.csv')
    weather = [getWeatherAtStop(index) for index, stop in stops[start:end].iterrows()]
    stopsT = stops[start:end].copy()
    stopsT['weather'] = weather
    stopsT.to_csv(filename)
    print(15,' done')

print('sleeping..')
# sleep(3700)
print('waking up..')
getWeatherAtAllStops()
