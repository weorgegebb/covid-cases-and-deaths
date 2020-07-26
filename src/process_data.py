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

    # Country case and death data
    for country in list(df["countriesAndTerritories"].unique()):
        country_table = df[df["countriesAndTerritories"] == country]
        json_output[country] = {
            "dates": list(country_table["dateRep"]),
            "cases": list(country_table["cases"]),
            "deaths": list(country_table["deaths"])
        }

    # All Data
    dates = list(df["dateRep"].unique())
    json_output["All"] = {"dates": dates, "cases": [], "deaths": []}

    for date in dates:
        total_cases = 0
        total_deaths = 0

        for country in list(df["countriesAndTerritories"].unique()):
            country_table = df[df["countriesAndTerritories"] == country]
            date_table = country_table[country_table["dateRep"] == date]
            if len(date_table["cases"].values) > 0:
                total_cases += int(date_table["cases"].values[0])
            if len(date_table["deaths"].values) > 0:
                total_deaths += int(date_table["deaths"].values[0])

        json_output["All"]["cases"].append(total_cases)
        json_output["All"]["deaths"].append(total_deaths)

    with open('./data/processed_data.json', 'w') as outfile:
        json.dump(json_output, outfile)


def main():
    download_data()
    process_data()


if __name__ == "__main__":
    main()