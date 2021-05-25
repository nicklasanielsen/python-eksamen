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
    return header

def select_All_Text ():
    soup = read_page()
    all_Text = soup.get_text()
    all_Text = all_Text.replace("\t", "").replace("\r", "").replace("\n", "")
    return all_Text

