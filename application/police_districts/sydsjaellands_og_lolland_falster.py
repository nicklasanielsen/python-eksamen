import bs4
import requests

from utils.crime_identifier import crime_identifier


class sydsjaellands_og_lolland_falster_handler:
    def fetch(link):
        def get_headlines(body):
            headlines = []
            data = {"description": "", "city": ""}

            for headline in body:
                tmp = headline.text

                headline_parts = tmp.split(": ")
                if len(headline_parts) == 2:
                    data["city"] = headline_parts[0]
                    data["description"] = headline_parts[1]
                    headlines.append(data.copy())

            return headlines

        def get_city(headlines):
            return headline["city"]

        def get_crime(headline):
            return crime_identifier.identify(headline["description"])

        def get_breakins_from_table(table):
            incident = {"city": "", "crime": ""}
            incidents = []

            data = bs4.BeautifulSoup(str(table), "html.parser")
            tmp = data.select("tbody > tr > td > strong")

            for row in tmp:
                value = row.text

                if (
                    value != "By"
                    and value != "Vej"
                    and value != "Type"
                    and value != "Tidsrum"
                    and value != "Udbytte"
                ):
                    incident["city"] = value
                    incident["crime"] = "indbrud"
                    incidents.append(incident.copy())

            return incidents

        def get_speed_from_table(table):
            incident = {"city": "", "crime": ""}
            incidents = []

            data = bs4.BeautifulSoup(str(table), "html.parser")
            tmp = data.select("tbody > tr")
            tmp.pop(0)

            for row in tmp:
                cols = bs4.BeautifulSoup(str(row), "html.parser")
                row_data = cols.select("td")

                city = row_data[0].text
                city = city.replace("\n", "")
                amount = row_data[5].text

                try:
                    amount = int(amount)
                except:
                    amount = 0

                for i in range(amount):
                    incident["city"] = city
                    incident["crime"] = "hastighedsoverskridelse"
                    incidents.append(incident.copy())

            return incidents

        def get_traffic_from_table(table):
            incident = {"city": "", "crime": ""}
            incidents = []

            data = bs4.BeautifulSoup(str(table), "html.parser")
            tmp = data.select("tbody > tr > td > strong")

            for row in tmp:
                value = row.text

                if value != "By" and value != "Vej" and value != "Tidspunkt":
                    incident["city"] = value
                    incident["crime"] = "færdsel"
                    incidents.append(incident.copy())

            return incidents

        def get_drugs_alcohol_from_table(table):
            incident = {"city": "", "crime": ""}
            incidents = []

            data = bs4.BeautifulSoup(str(table), "html.parser")
            tmp = data.select("tbody > tr > td > strong")

            for row in tmp:
                value = row.text

                if (
                    value != "By"
                    and value != "Vej"
                    and value != "Tidspunkt"
                    and value != "Person"
                    and value != "Sigtet for"
                ):
                    incident["city"] = value
                    incident["crime"] = "euforiserende stoffer"
                    incidents.append(incident.copy())

            return incidents

        reports = []
        data = {"city": "", "crime": ""}

        request = requests.get(link)
        request.raise_for_status()

        soup = bs4.BeautifulSoup(request.text, "html.parser")
        body = soup.select("div[class=rich-text] > p > strong")

        headlines = get_headlines(body)

        for headline in headlines:
            data["city"] = get_city(headline)
            data["crime"] = get_crime(headline)
            reports.append(data.copy())

        tables = soup.select("div[class=rich-text] > div[class=table-overflow] > table")

        try:
            table_breakin = bs4.BeautifulSoup(str(tables[0]), "html.parser")
            reports.extend(get_breakins_from_table(table_breakin))
        except:
            pass

        try:
            table_speed = bs4.BeautifulSoup(str(tables[1]), "html.parser")
            reports.extend(get_speed_from_table(table_speed))
        except:
            pass

        try:
            table_traffic = bs4.BeautifulSoup(str(tables[2]), "html.parser")
            reports.extend(get_traffic_from_table(table_traffic))
        except:
            pass

        try:
            table_drugs_alcohol = bs4.BeautifulSoup(str(tables[3]), "html.parser")
            reports.extend(get_drugs_alcohol_from_table(table_drugs_alcohol))
        except:
            pass

        return reports
