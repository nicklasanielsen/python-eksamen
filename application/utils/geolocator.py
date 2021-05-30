from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

locations = []

def locate(incident):
    print(incident["city"])
    for location in range(len(locations)):
        if location["city"] == incident["city"]:
            incident["latitude"] = location["latitude"]
            incident["longitude"] = location["longitude"]
            print("found!")
            return incident

    print("Looking..")
    geolocator = Nominatim(user_agent="cphbusiness-python-exam-newbiz")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

    country = "Denmark"

    loc = geocode(incident["city"])

    try:
        latitude = loc.latitude
        longitude = loc.longitude

        locations.append({"city":incident["city"],"latitude":latitude,"longitude":longitude})
    except:
        latitude = None
        longitude = None
    
    incident["latitude"]=latitude
    incident["longitude"]=longitude


    return incident