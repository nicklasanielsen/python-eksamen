import bs4
import requests


class bornholm_handler:
    def fetch(link):
        request = requests.get(link)
        request.raise_for_status()

        soup = bs4.BeautifulSoup(request.text, "html.parser")
        body = soup.select('div[class="rich-text"]')

        reports = []
        data = {"city": "", "crime": ""}

        return reports
