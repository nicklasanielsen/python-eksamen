from utils import data_fetcher
from utils import geolocator
from utils import mapper

import pandas as pd
import numpy as np


def main():
    print("Fetching..")
    data = data_fetcher.fetch("2021/05/29", "2021/05/30")

    cities = []
    crimes = []
    for d in data:
        cities.append(d["city"])
        crimes.append(d["crime"])

    crimes_set = set()
    counter_list = []
    dup_set = set()

    for c in range(len(crimes)):
        if c in crimes_set:
            continue
        crimes_set.add(crimes[c])

        counter = 0
        for i in range(len(crimes)):
            if crimes[c] == crimes[i] and cities[c] == cities[i]:
                counter += 1
        
        x = geolocator.locate(cities[c])[0]
        y = geolocator.locate(cities[c])[1]
        tmp =  (cities[c], crimes[c], counter, x,y)
        if tmp in dup_set:
            continue
        dup_set.add(tmp)
        counter_list.append((cities[c], crimes[c], counter, x,y))
        
    print(counter_list[0][0:3])



def test():
    cities=[]
    crimes=[]

    fetched_data = data_fetcher.fetch("2021/05/28", "2021/05/30")

    for report in fetched_data:
        if report["city"] not in cities:
            cities.append(report["city"])

        if report["crime"] not in crimes:
            crimes.append(report["crime"])

    tmp_list =[]

    for city in cities:
        city_crimes= []

        tmp = 0;
        for crime in crimes:
            amount = len(list(filter(lambda record: record["city"]== city and record["crime"]==crime, fetched_data)))
            tmp += amount

            city_crimes.append(amount)

        city_crimes.append(tmp)

        coordinates = geolocator.locate(city)
        city_crimes.append(coordinates[0])
        city_crimes.append(coordinates[1])


        tmp_list.append(city_crimes.copy())
        city_crimes.clear()

    crimes.append("i alt")
    crimes.append("latitude")
    crimes.append("longitude")

    df2 = pd.DataFrame(np.array(tmp_list), index=cities, columns=crimes)

    #print(df2)

    return mapper.draw(df2)


if __name__ == "__main__":
    test()