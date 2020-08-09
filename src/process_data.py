import requests
import pandas as pd
import json
import time


def download_data():
    url = "https://opendata.ecdc.europa.eu/covid19/casedistribution/csv"
    r = requests.get(url)
    with open('./data/downloaded_data.csv', 'wb') as f:
        f.write(r.content)
    print("Data Downloaded")


def process_data():
    df = pd.read_csv("./data/downloaded_data.csv")
    json_output = {}
    print("Read In Data")

    # Country case and death data
    start_time = time.time()
    for country in list(df["countriesAndTerritories"].unique()):
        country_table = df[df["countriesAndTerritories"] == country]
        json_output[country] = {
            "dates": list(country_table["dateRep"]),
            "cases": list(country_table["cases"]),
            "deaths": list(country_table["deaths"])
        }
    end_time = time.time()
    print(f"Calculated Country Cases and Deaths ({end_time - start_time}s)")

    # All Data
    start_time = time.time()
    dates = list(df["dateRep"].unique())
    json_output["All"] = {"dates": dates, "cases": [], "deaths": []}

    for date in dates:
        total_cases = df[df["dateRep"] == date]["cases"].sum()
        total_deaths = df[df["dateRep"] == date]["deaths"].sum()
        json_output["All"]["cases"].append(int(total_cases))
        json_output["All"]["deaths"].append(int(total_deaths))
    end_time = time.time()
    print(f"Calculated All Cases and Deaths ({end_time - start_time}s)")

    with open('./data/processed_data.json', 'w') as outfile:
        json.dump(json_output, outfile)
    print("Saved File")


def main():
    download_data()
    process_data()


if __name__ == "__main__":
    main()