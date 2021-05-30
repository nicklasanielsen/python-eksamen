from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

locations = []

def locate(city):
    for location in locations:
        if location["city"] == city:
            return location["latitude"], location["longitude"]

    geolocator = Nominatim(user_agent="cphbusiness-python-exam-newbiz")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

    country = "Denmark"

    loc = geocode(city +", " +country)

    try:
        latitude = loc.latitude
        longitude = loc.longitude

        locations.append({"city":city,"latitude":latitude,"longitude":longitude})
    except:
        latitude = None
        longitude = None
    
    
           
    return latitude,  longitude