from types import DynamicClassAttribute
import bs4
import requests
import re

def read_page ():
    r = requests.get('https://politi.dk/fyns-politi/doegnrapporter/fyns-politi-doegnrapport-20052021/2021/05/21')
    soup = bs4.BeautifulSoup(r.text, 'html.parser')
    return soup

def select_Segment ():
    soup = read_page()
    segment = soup.select('article[class=newsArticle]')
    return segment

def select_Headline ():
    soup = read_page()
    headline = soup.select('h1[class="h1-police-bold dark-blue"]')
    return headline

def select_Incident_Text ():
    soup = read_page()
    text = soup.findAll('p', attrs={'class' : None})
    return text

def select_Incident_Header ():
    soup = read_page()
    header = soup.findAll('h3', attrs={'class' : None})

    soup_str = soup_to_string(header)
        
    soup_str = soup_str.replace("<h3>", "").replace("</h3>", "").replace("\n", "").replace("/","").replace("\xa0","")

    return soup_str

def select_All_Text ():
    soup = read_page()
    all_Text = soup.get_text()
    all_Text = all_Text.replace("\t", "").replace("\r", "").replace("\n", "")
    return all_Text

def select_Incident ():
    soup = read_page()
    incident = soup.select('div[class="rich-text"]')

    return incident

def incident_Locations():
    regions = select_Incident_Header()
    cities = select_Incident()

    cities = soup_to_string(cities)

    list_of_cities = re.findall(r'\d{4} [A-Z][^\s]+', cities)
    list_of_regions = re.findall('[A-Z][^A-Z]*', regions)

    list_of_dicts = []

    region = list_of_regions[0]
    city_and_zipcode = list_of_cities[0]
    crimes = 0
    

    for i in range (len(list_of_cities)):
        dictt = {"Region" : region, "By og postnummer" : city_and_zipcode, "Antal af forbrydelser": crimes}



        if dictt.get("By og postnummer") == list_of_cities[i]:
            crimes +=1
            dictt.update({"Antal af forbrydelser": crimes})
        else:
            dictt.update({"By og postnummer": list_of_cities[i]})
            city_and_zipcode = dictt.get("By og postnummer")
            crimes = 1
            dictt.update({"Antal af forbrydelser": crimes})

        list_of_dicts.append(dictt)

    return list_of_dicts

def incident_Time():
    times = select_Incident()
    
    soup_str = soup_to_string(times)

    soup_str = soup_str.replace("<h3>", "").replace("</h3>", "").replace("\n", "").replace("/","").replace("\xa0","").replace("<p>", "")

    list_anmeldt = re.findall(r'\bAnmeldt: \d{8} \d{2}:\d{2}', soup_str)
    list_sket = re.findall(r'\bSket: \d{8} \d{2}:\d{2}', soup_str)
    list_of_sets = []

    for i in range (len(list_anmeldt)):
        incident_set = {list_anmeldt[i], list_sket[i]}
        list_of_sets.append(incident_set)

    return list_of_sets

def soup_to_string(soup_list):
    soup_str = ""
    for i in soup_list:
        soup_str = soup_str + str(i)

    return soup_str

