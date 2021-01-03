#!/usr/bin/env python
# coding: utf-8

"""
12/04/2020
Purpose: to generate a table with fake data for Holmes-Moriarty pandas/pyspark/sql puzzle.
"""
import sys

import pandas as pd

from faker import Faker
from faker.generator import random

from helpers import main_dict, weekday, remove_data_files
from helpers import identify_crime_type_country, identify_moriarty

from helpers import seed  # change the seed in helpers to change the generated data

random.seed(seed)
Faker.seed(seed)
faker = Faker()


def parse_main_dict():
    """Parses dict to get the lists of
    countries, cities, and fakers. Fakers allow generation of region specific fake data.
    Also generates total number of agents
    """
    Faker.seed(seed)  # required to generate reproducible data

    countries = main_dict.keys()
    cities = [v['city'] for v in main_dict.values()]
    fakers = [Faker(v['faker_abbrev']) for v in main_dict.values()]
    total_agents = sum([v['number_of_agents'] for v in main_dict.values()])

    return fakers, countries, cities, total_agents


def generate_lat_lon(country, main_dict):
    """
    Generates latitude and longitude for a city in the country.
    The values have a defined range of randomness near
    the city (the coordinates of the city are from the main_dict).
    """
    lats = []
    lons = []
    n_agents = main_dict[country]['number_of_agents']
    print("n_agents: ", n_agents)
    for i in range(n_agents):
        lat = float(main_dict[country]['city_coordinates'][0])
        lon = float(main_dict[country]['city_coordinates'][1])
        dev = 0.25
        min_lat, max_lat = lat - dev, lat + dev
        min_lon, max_lon = lon - dev, lon + dev
        round_to = 4
        lat1 = round(random.uniform(min_lat, max_lat), round_to)
        lon1 = round(random.uniform(min_lon, max_lon), round_to)
        lats.append(str(lat1))
        lons.append(str(lon1))

    return lats, lons


def generate_aliases(df, n_agents):
    """"""
    with open('./extra_data/aliases.txt', 'r') as f:
        aliases = [i.capitalize() for i in f.read().split()]

    aliases_unique = list(set(aliases))
    aliases = aliases_unique + ["" for i in range(n_agents - len(aliases_unique))]
    random.shuffle(aliases)

    df['alias'] = pd.Series(aliases)  # create a column from the list

    return df


def generate_country_criminals_df(regional_faker, country):
    """
    Creates a dataframe of criminals with columns: name, nickname, address, city,
    country, latitude, longitude using regional fakers using predefined and random
    values (number of agents) defined in the main dict.
    """

    n_agents = main_dict[country]['number_of_agents']

    name_col = [regional_faker.name() for i in range(n_agents)]
    address_col = [regional_faker.address().replace('\n', ' ') for i in
                   range(n_agents)]

    lats_col, lons_col = generate_lat_lon(country, main_dict)
    cols_data = [name_col, address_col, lats_col, lons_col]

    column_names = ['name', 'address', 'lat', 'lon']

    country_criminals_dict = {col: data for (col, data) in zip(column_names, cols_data)}
    df = pd.DataFrame(country_criminals_dict)

    # add columns of country and city
    df['country'] = country
    df['city'] = main_dict[country]['city']
    df['id'] = df.index

    df = df[['name', 'id', 'address', 'lat', 'lon', 'country', 'city']]

    return df


def add_date_weekday_column(df):
    """Creates random dates within the last year and adds it as 'datetime64' column """

    faker_en = Faker('en_GB')

    def date_using_faker(x):
        return faker_en.date_between(start_date='-360d', end_date='today')

    df['date'] = df['name'].apply(date_using_faker)  # can use any column; here we are using 'name'
    df['date'] = df['date'].astype('datetime64')

    df["weekday"] = df["date"].apply(weekday)

    return df


def add_date_not_sunday(value):
    """Creates fake date that is not a Sunday"""

    faker_en = Faker('en_GB')
    fake_date = faker_en.date_between(start_date='-360d', end_date='today')

    while weekday(fake_date) == 'Sunday':
        fake_date = faker_en.date_between(start_date='-360d', end_date='today')

    return fake_date


def add_moriarty_profile(df, crime_type_, country_):
    """Makes sure the solution's date is not 'Sunday' and alias is None."""

    df_moriarty = df.loc[(df.country == country_) & (df.crime_type == crime_type_)] \
        .sort_values('profit', ascending=False).reset_index()
    hidden_moriarty_name = df_moriarty.name[0]
    # print("Moriarty name: {}".format(hidden_moriarty_name))
    df_moriarty = df.loc[df.name == hidden_moriarty_name]
    df_moriarty = df_moriarty.copy()

    df_not_moriarty = df.loc[df.name != hidden_moriarty_name]

    df_moriarty["date"] = add_date_not_sunday('test')
    df_moriarty["date"] = df_moriarty["date"].astype('datetime64')
    df_moriarty['alias'] = ""

    df = pd.concat([df_not_moriarty, df_moriarty])

    return df


def add_crime_types(df):
    """
    Generates a column of crime types  for all criminals.
    Each type has its own defined fraction of all criminals to ensure
    weapons sales has the most sales (in money units) and
    that other crime types profits look realistic.
    """

    crimes_dict = {'weapons sale': {'factor': 100.0, 'fraction': 0.05},
                   'drug sale': {'factor': 9.0, 'fraction': 0.08},
                   'robbery': {'factor': 0.2, 'fraction': 0.17},
                   'forgery': {'factor': 0.12, 'fraction': 0.10},
                   'theft': {'factor': 0.08, 'fraction': 0.4},
                   'pickpocketing': {'factor': 0.01, 'fraction': 0.2}
                   }

    full_crimes_list = []
    for k in list(crimes_dict.keys()):
        if k != list(crimes_dict.keys())[-1]:
            times = int(df.shape[0] * crimes_dict[k]['fraction'])
        else:
            times = df.shape[0] - len(full_crimes_list)
        crimes = [k for i in range(times)]
        full_crimes_list += crimes

    random.shuffle(full_crimes_list)

    df['crime_type'] = full_crimes_list

    def generate_criminal_profits(crime_type):
        """
        Adds profit information for each criminal.
        Factor from the dict is used to make crime types profits look realistic
        """
        return int(-(crimes_dict[crime_type]['factor'] * (-random.randrange(100, 5000, 10)) // 1))

    df['profit'] = df['crime_type'].apply(generate_criminal_profits)

    return df


def split_main_df_into_countries(df):
    """
    Splits the main df into 5 dfs based on the country for unioning in the test.
    Include columns: name, alias, lat, lon.
    (with names specific to the corresponding countries).
    Save to the current folder.
    """
    df_all_countries = df.copy()

    country_list = df_all_countries["country"].unique().tolist()

    dfs_dict = {}
    for num, country_ in enumerate(country_list):

        df_country = df_all_countries.loc[(df_all_countries.country == country_)]
        df = df_country.copy()
        df = df[["id", "name", "alias", "lat", "lon"]]

        # add country-specific column names
        if country_ == "Germany" or country_ == "Netherlands":
            cols = ["id", "benennen", "aliasnamen", "breitengrad", "länge"]
        elif country_ == "France":
            cols = ["id", "nom", "pseudonyme", "latitude", "longitude"]
        else:
            cols = ["id", "name", "alias", "latitude", "longitude"]

        # assign new column names
        df.columns = cols
        # save as file with country name
        file_name = "./data/criminals_{}.csv".format(country_)
        print("Saved: {}".format(file_name))
        df.to_csv(file_name, header=True, index=False)

        # generate crime_type, profit csvs
        df = df_country.copy()
        df = df[["name", "crime_type", "profit"]]
        file_name = "./data/crime_type_profit_{}.txt".format(country_)
        print("Saved: {}".format(file_name))
        df.to_csv(file_name, sep=' ', header=True, index=False)


def save_id_date_df(df):
    """
    Adds date of the last crime. Leave only 'id' and 'date' (for joining on id)
    """

    df_id_date = df[["id", "date", "country"]]
    file_name = "./data/id_dates.csv"
    df_id_date.to_csv(file_name, header=True, index=False)
    print("Saved: {}".format(file_name))


def generate_df_with_criminals():
    """
    Creates a pandas dataframe of criminals for all countries.
    1.Generates aliases.
    2. Iterates over countries to create dataframe of criminals per country.
    3. Combines all country dfs into the main dataframe.
    """
    remove_data_files()

    fakers, countries, cities, n_agents = parse_main_dict()

    # creates the backbone of the future df with criminals using regional fakers
    country_criminals_dfs = []
    for faker, country in zip(fakers, countries):
        df = generate_country_criminals_df(faker, country)
        country_criminals_dfs.append(df)
    df = pd.concat(country_criminals_dfs, ignore_index=True, sort=False)

    df = generate_aliases(df, n_agents)  # from a .txt file

    print("Initial shape: {}".format(df.shape[0]))
    df.drop_duplicates(subset=['name'], inplace=True)
    print("Initial shape deduped by name: {}".format(df.shape[0]))

    # add date, weekday columns
    df = add_date_weekday_column(df)

    # add crime_type and profit columns
    df = add_crime_types(df)

    # select columns and set their order
    df = df[['name', 'alias', 'id', 'address', 'lat', 'lon', 'country',
             'city', 'date', 'crime_type', 'profit', 'weekday']]
    df[["name"]].drop_duplicates()

    # generating solution
    crime_type_, country_ = identify_crime_type_country(df)

    df = add_moriarty_profile(df, crime_type_, country_)
    print("Final shape: {}".format(df.shape[0]))

    identify_moriarty(df, seed, save=True)

    # generating data
    split_main_df_into_countries(df)  # saves csvs

    save_id_date_df(df)  # save id and date for future join

    return df


if __name__ == '__main__':
    try:
        print("Starting data generation for the puzzle")
        main_criminals_df = generate_df_with_criminals()
        print("main_criminals_df count: {}".format(main_criminals_df.shape[0]))

    except Exception:
        print("Exception starting generate_df_with_criminals.")
        print(sys.exc_info())
        sys.exit(0)
