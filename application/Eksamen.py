from utils import data_fetcher
from utils import geolocator

from concurrent.futures.thread import ThreadPoolExecutor


def main():
    print("Fetching..")
    data = data_fetcher.fetch("2021/05/28", "2021/05/30")

    print("Locating")

    with ThreadPoolExecutor(25) as ex:
        tmp = ex.map(geolocator.locate, data)

    print(list(tmp))


if __name__ == "__main__":
    main()
