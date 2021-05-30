import bs4
import requests
import re
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import gmaps
import gmaps.datasets
import ipywidgets as widgets

gmaps.configure(api_key='AIzaSyCV7H6JuYtk0sh8EE8bn4Czh9aTRdmQLiQ')

# Reads the page of the link
def read_page(link):
    r = requests.get(link)
    soup = bs4.BeautifulSoup(r.text, 'html.parser')
    return soup


def select_Segment(link):
    soup = read_page(link)
    segment = soup.select('article[class=newsArticle]')
    return segment


def select_Headline(link):
    soup = read_page(link)
    headline = soup.select('h1[class="h1-police-bold dark-blue"]')
    return headline


def select_Incident_Text(link):
    soup = read_page(link)
    text = soup.findAll('p', attrs={'class': None})
    return text

# Selects the header of the incident


def select_Incident_Header(link):
    soup = read_page(link)
    header = soup.findAll('h3', attrs={'class': None})

    soup_str = soup_to_string(header)

    soup_str = soup_str.replace("<h3>", "").replace(
        "</h3>", "").replace("\n", "").replace("/", "").replace("\xa0", "")

    return soup_str


def select_All_Text(link):
    soup = read_page(link)
    all_Text = soup.get_text()
    all_Text = all_Text.replace("\t", "").replace("\r", "").replace("\n", "")
    return all_Text


def select_Incident(link):
    soup = read_page(link)
    incident = soup.select('div[class="rich-text"]')

    return incident


def select_Incident_Crimes(link):
    crimes = select_Incident(link)

    soup_str = soup_to_string(crimes)

    soup_str = soup_str.replace("<h3>", "").replace(
        "</h3>", "").replace("\n", "").replace("/", "").replace("\xa0", "").replace("<br>", "")

    return soup_str

# Helper function for incident_Locations


def get_crimes(dicts):
    return dicts.get("Antal af forbrydelser")


def incident_Locations(link):
    regions = select_Incident_Header(link)
    cities = select_Incident(link)

    cities = soup_to_string(cities)

    list_of_cities = re.findall(r'\d{4} [A-ZÆØÅ][^\s]+', cities)
    list_of_cities.sort(reverse=True)
    list_of_regions = re.findall('[A-ZÆØÅ][^A-ZÆØÅ]*', regions)

    list_of_dicts = []

    region = list_of_regions[0]
    city_and_zipcode = list_of_cities[0]
    crimes = 0

    for i in range(len(list_of_cities)):
        dictt = {"Region": region, "By og postnummer": city_and_zipcode,
                 "Antal af forbrydelser": crimes}

        if dictt.get("By og postnummer") == list_of_cities[i]:
            crimes += 1
            dictt.update({"Antal af forbrydelser": crimes})
        else:
            dictt.update({"By og postnummer": list_of_cities[i]})
            city_and_zipcode = dictt.get("By og postnummer")
            crimes = 1
            dictt.update({"Antal af forbrydelser": crimes})

        list_of_dicts.append(dictt)
        list_of_dicts.sort(key=get_crimes, reverse=True)

    return list_of_dicts


def csv_cities(links):
    # csv file is from here https://www.postnord.dk/kundeservice/kundeservice-erhverv/om-postnumre/postnummerkort-postnummerfiler
    df = pd.read_csv('./postnumre.csv', sep=';')
    cities_set = set(df['BYNAVN'])
    cities_list = []
    for link in links:
        stringg = select_Incident_Crimes(link)
        for city in cities_set:
            if city in stringg:
                count = sum(1 for _ in re.finditer(
                    r'\b%s\b' % re.escape(city), stringg))
                cities_list.append((city, count))

    return(cities_list)


def incidents_for_cities(links):
    result_list = []
    for i in links:
        locations = incident_Locations(i)
        list_of_sets = []
        city = ""
        crimes = ""

        for i in range(len(locations)):
            city = locations[i].get("By og postnummer")
            crimes = locations[i].get("Antal af forbrydelser")
            setset = (city, crimes)

            list_of_sets.append(setset)

        cities_set = set()

        for i in range(len(list_of_sets)):
            if list_of_sets[i][0] in cities_set:
                continue
            else:
                cities_set.add(list_of_sets[i][0])
                result_list.append(list_of_sets[i])

    return result_list


def calculate_crimes(links):
    listt = csv_cities(links)
    cities = []
    crimes_counter = []
    for i in listt:
        cities.append(i[0])
        crimes_counter.append(i[1])

    cset = set()
    counter_list = []

    for city in cities:
        if city in cset:
            continue
        cset.add(city)

        counter = 0
        for i in range(len(cities)):
            if city == cities[i]:
                counter += crimes_counter[i]
        counter_list.append((city, counter))

    return counter_list

    return result_list


def incident_Time(link):
    times = select_Incident(link)

    soup_str = soup_to_string(times)

    soup_str = soup_str.replace("<h3>", "").replace("</h3>", "").replace("\n", "").replace("/", "").replace("\xa0", "").replace("<p>", "")

    list_anmeldt = re.findall(r'\bAnmeldt: \d{8} \d{2}:\d{2}', soup_str)
    list_sket = re.findall(r'\bSket: \d{8} \d{2}:\d{2}', soup_str)
    list_of_sets = []

    for i in range(len(list_anmeldt)):
        incident_set = {list_anmeldt[i], list_sket[i]}
        list_of_sets.append(incident_set)

    return list_of_sets


def soup_to_string(soup_list):
    soup_str = ""
    for i in soup_list:
        soup_str = soup_str + str(i)

    return soup_str


def plotting(links):
    cities_list = []
    crimes_list = []
    list_for_plotting = calculate_crimes(links)

    for i in range(len(list_for_plotting)):
        cities_list.append(list_for_plotting[i][0])
        crimes_list.append(list_for_plotting[i][1])

    df = pd.DataFrame({"City": cities_list, "Crimes": crimes_list})
    df_sorted = df.sort_values(by=['Crimes'])

    plt.figure(figsize=[20, 10])
    plt.xticks(rotation=45, horizontalalignment='right')
    plt.ylabel("Amount of incidents", fontsize=10)
    plt.bar(df_sorted.loc[:, "City"], df_sorted.loc[:, "Crimes"])
    plt.show()


def draw_heatmap(links):
    cities_list = []
    crimes_list = []
    latitude_list = []
    longitude_list = []
    list_for_plotting = calculate_crimes(links)
    df = pd.read_csv('./geolocations.csv', sep=';')

    for i in range(len(list_for_plotting)):
        cities_list.append(list_for_plotting[i][0])
        crimes_list.append(list_for_plotting[i][1])

    for i in range(len(cities_list)):
        for j in range(len(df)):
            if (df.iloc[j]['BYNAVN'] == cities_list[i]):
                latitude_list.append(df.iloc[j]['LATITUDE'])
                longitude_list.append(df.iloc[j]['LONGITUDE'])

    heatmap_Data = {'latitude': latitude_list, 'longitude': longitude_list, 'incidents': crimes_list}
    heatmap_DF = pd.DataFrame(heatmap_Data, index=cities_list)

    #data = {'latitude': [55.8839278], 'longitude': [12.4974012], 'incidents': [10]}
    #df = pd.DataFrame(data)

    locations = heatmap_DF[['latitude', 'longitude']]
    weights = heatmap_DF['incidents']

    fig = gmaps.figure()
    fig.add_layer(gmaps.heatmap_layer(locations, weights=weights))
    return fig

    #widgets.IntSlider()