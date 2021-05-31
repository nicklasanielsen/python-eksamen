import bs4
import requests

from application.utils.crime_identifier import crime_identifier


class nordjylland_handler:
    def fetch(link):
        def get_headlines(body):
            headlines = []
            data = {"description": "", "city": ""}

            for headline in body:
                tmp = headline.text

                tmp = tmp.replace(
                    "Færdselsbetjente kontrollerede bilist – endte med 8 sigtelser", ""
                ).replace(
                    "\n", ""
                )  # Link to another article

                headline_parts = tmp.split(" – ")
                if len(headline_parts) == 2:
                    data["city"] = headline_parts[0]
                    data["description"] = headline_parts[1]
                    headlines.append(data.copy())

            return headlines

        def get_city(location):
            return location["city"]

        def get_crime(headline):
            return crime_identifier.identify(headline["description"])

        reports = []
        data = {"city": "", "crime": ""}

        request = requests.get(link)
        request.raise_for_status()

        soup = bs4.BeautifulSoup(request.text, "html.parser")
        body = soup.select("div[class=rich-text] > h2")

        headlines = get_headlines(body)

        for headline in headlines:
            data["city"] = get_city(headline)
            data["crime"] = get_crime(headline)
            reports.append(data.copy())

        return reports
