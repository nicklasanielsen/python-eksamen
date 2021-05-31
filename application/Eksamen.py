from application.utils import data_fetcher
from application.utils import geolocator
from application.utils import mapper
from application.utils import charter

import pandas as pd
import numpy as np


def prepare_data(start_date, end_date):
    print("Preparing to gather the requested data..")
    cities = []
    crimes = []

    fetched_data = data_fetcher.fetch(start_date, end_date)

    if len(fetched_data) == 0:
        print("No valid data found")
        return

    print("Creating dataframe..")

    for report in fetched_data:
        if report["city"] not in cities:
            cities.append(report["city"])

        if report["crime"] not in crimes:
            crimes.append(report["crime"])

    tmp_list = []

    for city in cities:
        city_crimes = []

        tmp = 0
        for crime in crimes:
            amount = len(
                list(
                    filter(
                        lambda record: record["city"] == city
                        and record["crime"] == crime,
                        fetched_data,
                    )
                )
            )
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

    df2 = df2.dropna()

    print("Dataframe created.")

    return df2


def map(start_date, end_date, crime="i alt"):
    data = prepare_data(start_date, end_date)

    if len(data) == 0:
        return

    data.drop(
        data.columns.difference([crime, "latitude", "longitude"]), 1, inplace=True
    )

    return mapper.draw(data)


def chart(start_date, end_date, column="i alt"):
    data = prepare_data(start_date, end_date)

    if len(data) == 0:
        return

    return charter.plotter(data, column)
