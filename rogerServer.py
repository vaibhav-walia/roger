import sys
import googlemaps
import pyowm
import pandas as pd
import numpy as np
import geopy.distance
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import os
import time
import datetime
from flask import Flask, render_template, request, jsonify, abort

OWM_API_KEY = sys.argv[1] #weather api key should be passed as first argument
MAP_API_KEY = sys.argv[2] #gmap api key should be passed as second argument

owm = pyowm.OWM(OWM_API_KEY)
gmaps = googlemaps.Client(key=MAP_API_KEY)
stops = pd.DataFrame()

# instantiate a chrome options object so you can set the size and headless preference
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")

app = Flask(__name__)

@app.route('/')
def serve_app():
    return render_template('roger.html')

@app.route('/roger/api/combined')
def serve_combined():
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    if(lat==None or lng==None):
        abort(422)
    else:
        weather = getWeather(float(lat),float(lng))
        bus = scrape_bus_data(float(lat),float(lng))
        response = jsonify({'weather':weather,'bus':bus})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

@app.route('/roger/api/weather')
def serve_weather_data():
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    if(lat==None or lng==None):
        abort(422)
    else:
        status = getWeather(float(lat),float(lng))
        return jsonify({'status': status})

@app.route('/roger/api/bus')
def serve_bus_data():
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    if(lat==None or lng==None):
        abort(422)
    else:
        bus_info = scrape_bus_data(float(lat),float(lng))
        return jsonify({'bus_info': bus_info})

'''Finds the nearest bus stop to the lat lng passed in and returns a dictioanry
containing the nearest stop name and another dictionary of atmost 5 buses arriving
at the bus stop'''
def scrape_bus_data(lat,lng):
    cls_stop_code = closest_stop(lat,lng)
    cls_stop_name = stops.loc[cls_stop_code]['stop_name']
    print(cls_stop_name)

    '''Get the buses at this stop'''
    # chromedriver binary MUST be put in the same directory as this file
    chrome_driver = os.getcwd()+'/chromedriver';

    # go to transit website
    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)
    driver.get("https://truetime.portauthority.org/bustime/eta/eta.jsp")

    #find stop number input box
    stpNumInput = driver.find_element_by_id("txtFindStopID")

    #enter stop number
    stpNumInput.send_keys(cls_stop_code)

    #click the find button
    findStop_button = driver.find_element_by_id("findStop")
    findStop_button.click()

    #get the first bus data
    bus_data = {}
    for i in range(1,6):
        route = "route" + str(i)
        eta = "time" + str(i)
        busNumber = (driver.find_element_by_id(route).text).strip()
        eta = (driver.find_element_by_id(eta).text).strip()
        if busNumber != '' and eta != '':
            bus_data[i] = {'bus':busNumber, 'eta':eta}

    #return bus and stop Data
    data = {}
    data['stp_name'] = cls_stop_name
    data['bus_data'] = bus_data
    return data

'''Finds the closet stop to the given lat, lng'''
def closest_stop(lat,lng):
    global stops
    """ Loop through the stops to find the closest """
    #read stop data only once
    if stops.empty:
        getStopInfo()

    cl_stp = None #closet stop
    min = 99999999999999 # a very big value for distance
    myloc = (float(lat),float(lng))

    for index, row in stops.iterrows():
        lt = row['stop_lat']
        ln = row['stop_lon']
        stoploc = (lt,ln)
        distance = geopy.distance.vincenty(myloc, stoploc).miles
        if(distance<min):
            min = distance
            cl_stp = index

    print(cl_stp)
    return cl_stp

'''Calls the weather api to get weather at a particular latitute and
longitutde '''
def getWeather(lat,lng):
    obs = owm.weather_at_coords(lat,lng)
    #print(lat,',',lng,':',obs.get_weather().get_status())
    #return obs.get_weather().get_status()
    obs_weather = obs.get_weather()
    weather = {}
    weather['status'] = obs_weather.get_status()
    weather['detailed_status'] = obs_weather.get_detailed_status()
    weather['weather_code'] = obs_weather.get_weather_code()
    weather['weather_icon_name'] = obs_weather.get_weather_icon_name()
    weather['icon'] = 'http://openweathermap.org/img/w/'+weather['weather_icon_name']+'.png'
    weather['recommendation'] = getRecommendation(weather['weather_code'])
    return weather

'''Reads the stop info from stops.txt'''
def getStopInfo():
    global stops
    stops = pd.read_csv('stops.txt',index_col='stop_code')

def getRecommendation(code):
    map = {
    200 : 'Get an umbrella!',
    201 : 'Get an umbrella!',
    202 : 'Get an umbrella!',
    210 : 'Get an umbrella!',
    211 : 'Get an umbrella!',
    212 : 'Get an umbrella!',
    221 : 'Get an umbrella!',
    230 : 'Get an umbrella!',
    231 : 'Get an umbrella!',
    232 : 'Get an umbrella!',
    300	: 'Get an umbrella!',
    301	: 'Get an umbrella!',
    302	: 'Get an umbrella!',
    310	: 'Get an umbrella!',
    311	: 'Get an umbrella!',
    312	: 'Get an umbrella!',
    313	: 'Get an umbrella!',
    314	: 'Get an umbrella!',
    321 : 'Get an umbrella!',
    500	: 'Get an umbrella!',
    501	: 'Get an umbrella!',
    502	: 'Get an umbrella!',
    503	: 'Get an umbrella!',
    504	: 'Get an umbrella!',
    511	: 'Get an umbrella!',
    520	: 'Get an umbrella!',
    521	: 'Get an umbrella!',
    522	: 'Get an umbrella!',
    531	: 'Get an umbrella!',
    600	: 'Layer up!',
    601	: 'Layer up!',
    602	: 'Layer up!',
    611	: 'Get an umbrella and layer up!',
    612	: 'Get an umbrella and layer up!',
    615	: 'Get an umbrella and layer up!',
    616	: 'Get an umbrella and layer up!',
    620	: 'Get an umbrella and layer up!',
    621	: 'Get an umbrella and layer up!',
    622	: 'Get an umbrella and layer up!',
    701	: 'Get a light jacket',
    711	: 'Avoid travel',
    721	: 'All set!',
    731	: 'Dusty! Stay safe',
    741	: 'Avoid travel',
    751	: 'All set!',
    761	: 'All set!',
    762	: 'Avoid travel',
    771	: 'Avoid travel',
    781	: 'Avoid travel',
    800	: 'Sunglasses!',
    801	: 'Get an umbrella!',
    802	: 'Get an umbrella!',
    803	: 'Get an umbrella!',
    804	: 'Get an umbrella!',
    }
    return map.get(code)

if __name__ == '__main__':
    app.run()
