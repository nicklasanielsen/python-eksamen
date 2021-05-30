from concurrent.futures.thread import ThreadPoolExecutor
from time import sleep

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from police_districts.bornholm import bornholm_handler
from police_districts.fyn import fyn_handler
from police_districts.koebenhavns_vestegn import koebenhavns_vestegn_handler
from police_districts.midt_og_vestsjaelland import midt_og_vestsjaelland_handler
from police_districts.nordjylland import nordjylland_handler
from police_districts.nordsjaelland import nordsjaelland_handler
from police_districts.oestjylland import oestjylland_handler
from police_districts.sydsjaellands_og_lolland_falster import (
    sydsjaellands_og_lolland_falster_handler,
)


def fetch_report_links(start_date, end_date):
    page = 1

    options = Options()
    options.headless = True

    browser = webdriver.Firefox(options=options)

    report_links = []

    while True:
        url = (
            "https://politi.dk/doegnrapporter?fromDate="
            + start_date
            + "&toDate="
            + end_date
            + "&newsType=D%C3%B8gnrapporter&page="
            + str(page)
        )

        browser.get(url)
        print("Requesting: " + url)
        sleep(3)

        links = browser.find_elements_by_class_name("newsResultLink")

        if links:
            for link in links:
                report_links.append(link.get_attribute("href"))

            page += 1
        else:
            break

    browser.close()

    return report_links


def district_sorter(links=[]):
    districts = {
        "bornholm": [],
        "fyn": [],
        "koebenhavns_vestegn": [],
        "midt_og_vestsjaelland": [],
        "nordjylland": [],
        "nordsjaelland": [],
        "oestjylland": [],
        "sydsjaellands_og_lolland_falster": [],
    }

    for link in links:
        if "bornholms-politi" in link:
            districts["bornholm"].append(link)
        elif "fyns-politi" in link:
            districts["fyn"].append(link)
        elif "koebenhavns-vestegns-politi" in link:
            districts["koebenhavns_vestegn"].append(link)
        elif "midt-og-vestsjaellands-politi" in link:
            districts["midt_og_vestsjaelland"].append(link)
        elif "nordjyllands-politi" in link:
            districts["nordjylland"].append(link)
        elif "nordsjaellands-politi" in link:
            districts["nordsjaelland"].append(link)
        elif "sydsjaellands-og-lolland-falsters-politi" in link:
            districts["sydsjaellands_og_lolland_falster"].append(link)
        elif "oestjyllands-politi" in link:
            districts["oestjylland"].append(link)

    return districts


def get_incidents(reports=[]):
    incidents = []

    for report in reports:
        incidents.extend(report)

    return incidents


def fetch_incidents(districts={}, workers=25):
    incidents = []

    with ThreadPoolExecutor(workers) as ex:
        bornholm = ex.map(bornholm_handler.fetch, districts.get("bornholm"))
        fyn = ex.map(fyn_handler.fetch, districts.get("fyn"))
        koebenhavns_vestegn = ex.map(
            koebenhavns_vestegn_handler.fetch,
            districts.get("koebenhavns_vestegn"),
        )
        midt_og_vestsjaelland = ex.map(
            midt_og_vestsjaelland_handler.fetch,
            districts.get("midt_og_vestsjaelland"),
        )
        nordjylland = ex.map(nordjylland_handler.fetch, districts.get("nordjylland"))
        nordsjaelland = ex.map(
            nordsjaelland_handler.fetch, districts.get("nordsjaelland")
        )
        sydsjaellands_og_lolland_falster = ex.map(
            sydsjaellands_og_lolland_falster_handler.fetch,
            districts.get("sydsjaellands_og_lolland_falster"),
        )
        oestjylland = ex.map(oestjylland_handler.fetch, districts.get("oestjylland"))

        # incidents.extend(get_incidents(bornholm))
        incidents.extend(get_incidents(fyn))
        # incidents.extend(get_incidents(koebenhavns_vestegn))
        incidents.extend(get_incidents(midt_og_vestsjaelland))
        incidents.extend(get_incidents(nordjylland))
        incidents.extend(get_incidents(nordsjaelland))
        incidents.extend(get_incidents(sydsjaellands_og_lolland_falster))
        # incidents.extend(get_incidents(oestjylland))

    return incidents


def fetch(start_date, end_date):
    links = fetch_report_links(start_date, end_date)
    sorted_links = district_sorter(links)

    incidents = fetch_incidents(sorted_links)

    return incidents
