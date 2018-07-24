import sys
import googlemaps
import pyowm

OWM_API_KEY = sys.argv[1]
MAP_API_KEY = sys.argv[2]

owm = pyowm.OWM(OWM_API_KEY)
gmaps = googlemaps.Client(key=MAP_API_KEY)


'''Returns a dictionary containing current latitute and longitutde'''
def getLocation():
    return (gmaps.geolocate())['location'];

def getWeather(lat,lng):
    obs = owm.weather_at_coords(lat,lng)
    print(lat,',',lng,':',obs.get_weather().get_status())


loc = getLocation()
lat = loc['lat']
lng = loc['lng']

getWeather(90,180)

for lat in range(-90,91):
    for lng in range(-180,181):
        getWeather(lat,lng)
