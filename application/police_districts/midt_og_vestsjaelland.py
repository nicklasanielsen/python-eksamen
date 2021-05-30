import bs4
import requests
from requests.api import head

from utils.crime_identifier import crime_identifier


class midt_og_vestsjaelland_handler:
    def fetch(link):
        def get_headlines(body):
            headlines = []
            data = {"description": "", "city": ""}

            for headline in body:
                tmp = headline.text

                headline_parts = tmp.split(" – ")
                if len(headline_parts) == 2:
                    data["description"] = headline_parts[0]
                    data["city"] = headline_parts[len(headline_parts) - 1]
                    headlines.append(data.copy())

            return headlines

        def get_city(headline):
            tmp = headline["city"]
            tmp = tmp.split(", ")

            return tmp[len(tmp) - 1]

        def get_crime(headline):
            return crime_identifier.identify(headline["description"])

        reports = []
        data = {"city": "", "crime": ""}

        request = requests.get(link)
        request.raise_for_status()

        soup = bs4.BeautifulSoup(request.text, "html.parser")
        body = soup.select("div[class=rich-text] > h3")

        headlines = get_headlines(body)

        for headline in headlines:
            data["city"] = get_city(headline)
            data["crime"] = get_crime(headline)
            reports.append(data.copy())

        return reports
