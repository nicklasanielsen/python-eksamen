from geopy.geocoders import Nominatim


def locate(incident):
    print(incident)
    geolocator = Nominatim(user_agent="min mor")

    country = "Denmark"

    loc = geolocator.geocode(
        incident["city"] + ", " + country, exactly_one=True, timeout=60
    )

    try:
        incident["latitude"] = loc.latitude
        incident["longitude"] = loc.longitude
    except:
        incident["latitude"] = None
        incident["longitude"] = None

    return incident
