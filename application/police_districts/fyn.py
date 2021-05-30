import bs4
import requests
import re

from utils.crime_identifier import crime_identifier


class fyn_handler:
    def fetch(link):
        def get_locations(body=""):
            return re.findall(r"\d{4} [A-ZÆØÅ][^\s]+", body)

        def get_city(location=""):
            return re.findall(r"[A-ZÆØÅ][^\s]+", location)[0]

        def get_crime(headline=""):
            return crime_identifier.identify(headline)

        reports = []
        data = {"city": "", "crime": ""}

        request = requests.get(link)
        request.raise_for_status()

        soup = bs4.BeautifulSoup(request.text, "html.parser")
        body = soup.select('div[class="rich-text"]')

        locations = get_locations(str(body))

        for location in locations:
            data["city"] = get_city(location)
            data["crime"] = get_crime("")
            reports.append(data.copy())

        return reports
