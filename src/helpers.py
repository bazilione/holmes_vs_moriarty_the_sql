import os
from faker.generator import random
import pandas as pd
from datetime import datetime

from faker import Faker
from faker.generator import random

seed = 1234
Faker.seed(seed)
faker = Faker()

main_dict = {
    'France':
         {'number_of_agents': random.randint(250, 350),
          'city': 'Paris',
          'city_coordinates': ('48.8566', '2.3522'),
          'faker_abbrev': 'fr_FR'},
    'United Kingdom':
         {'number_of_agents': random.randint(250, 350),
          'city': 'London',
          'city_coordinates': ('51.5074', '-0.1278'),
          'faker_abbrev': 'en_GB'},
    'Germany':
         {'number_of_agents': random.randint(250, 350),
          'city': 'London',
          'city_coordinates': ('50.1109', '8.6821'),
          'faker_abbrev': 'de_DE'},
    'Netherlands':
         {'number_of_agents': random.randint(250, 350),
          'city': 'Amsterdam',
          'city_coordinates': ('52.3667', '4.8945'),
          'faker_abbrev': 'nl_NL'}
     }


def remove_data_files():
    """Removes files in './data' folder for saving new files"""
    os.system('rm -f ./data/*')


def identify_crime_type_country(df):
    """Determines the crime type  and the country with largest aggregated profit"""
    df_by_profit = df.groupby(["crime_type"]) \
        .agg({"profit": "sum"}) \
        .sort_values("profit", ascending=False) \
        .reset_index()

    crime_type_big_sales = df_by_profit["crime_type"][0]
    print("crime_type_big_sales: {}".format(crime_type_big_sales))

    countries_crime_type_profit_df = df.loc[
        df["crime_type"] == "{}".format(crime_type_big_sales)] \
        .groupby(["country"]) \
        .agg({"profit": "sum"}) \
        .sort_values('profit', ascending=False) \
        .reset_index()

    country_with_top_sales = countries_crime_type_profit_df.country.tolist()[0]
    print("country_with_top_sales: {}".format(country_with_top_sales))

    return crime_type_big_sales, country_with_top_sales


def identify_moriarty(df, seed, save=True):
    """
    Emulates final stages of the solution.
    Using the main df that contains all columns determines
    moriarty_name and saves to './solution' folder.
    """
    crime_type_big_sales, country_with_top_sales = identify_crime_type_country(df)

    df = df.loc[
                    (df["crime_type"] == crime_type_big_sales) &
                    (df["country"] == country_with_top_sales) &
                    (df.alias == "") &
                    (df.weekday != "Sunday")
                    ]

    df = df.sort_values('profit', ascending=False).reset_index()

    moriarty_name = df.name[0]
    # print("Identified moriarty_name: {}".format(moriarty_name))

    if save:
        with open('./solution/moriarty_name.txt', 'w') as f:
            f.write("Name: {}.\n".format(moriarty_name))
            f.write("seed: {}.\n".format(str(seed)))
            now_string = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
            f.write("write datetime: {}.\n".format(now_string))

    return moriarty_name


def weekday(date):
    """ Generate day of the week based on date (as string or as datetime object)"""

    if isinstance(date, str):
        from datetime import datetime

        date = datetime.strptime(date, "%m-%d-%Y")  # change the format if necessary # "%Y-%m-%d"

    return date.strftime("%A")
