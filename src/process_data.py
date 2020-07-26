import requests
import pandas as pd
import json


def download_data():
    url = "https://opendata.ecdc.europa.eu/covid19/casedistribution/csv"
    r = requests.get(url)
    with open('./data/downloaded_data.csv', 'wb') as f:
        f.write(r.content)


def process_data():
    df = pd.read_csv("./data/downloaded_data.csv")
    json_output = {}

    for country in list(df["countriesAndTerritories"].unique()):
        country_table = df[df["countriesAndTerritories"] == country]
        json_output[country] = {
            "dates": list(country_table["dateRep"]),
            "cases": list(country_table["cases"]),
            "deaths": list(country_table["deaths"])
        }

    with open('./data/processed_data.json', 'w') as outfile:
        json.dump(json_output, outfile)


def main():
    download_data()
    process_data()


if __name__ == "__main__":
    main()