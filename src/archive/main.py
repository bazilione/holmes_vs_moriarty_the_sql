"""
name, address, country, coordinates, job, company, current_location, birthday,
catch_phrase, word, words, (characteristic_features), latitude, longitude

1165 total criminals:

2019/10/30
Purpose: generate a table with fake data
"""

import pandas as pd
import random

from faker import Faker
faker = Faker()
faker_fr = Faker('fr_FR')
faker_en = Faker('en_GB')
faker_de = Faker('de_DE')
faker_nl = Faker('nl_NL')

emails = []
names = []
addresses = []

# 'faker_region': 'fr_Fr'

main_dict = {'France':
                    {'number_of_agents': 324,
                    'city': 'Paris',
                    'city_coordinates': ('48.8566', '2.3522'),
                    'faker_abbriv': 'fr_FR'
                                      },
            'United Kingdom': {'number_of_agents': 450, 'city': 'London',
                    'city_coordinates': ('51.5074', '-0.1278'),
                               'faker_abbriv': 'en_GB'},
            'Germany': {'number_of_agents': 251, 'city': 'London',
                    'city_coordinates': ('50.1109', '8.6821'),
                        'faker_abbriv': 'de_DE'},
            'Netherlands': {'number_of_agents': 140, 'city': 'Amsterdam',
             'city_coordinates': ('52.3667', '4.8945'), 'faker_abbriv':
                                'nl_NL'}
            }


print(main_dict['France']['city_coordinates'][0])


def generate_lat_lon(country):
    lats = []
    lons = []
    n_agents = main_dict[country]['number_of_agents']
    print("n_agents: ", n_agents)
    for i in range(n_agents):
        lat = float(main_dict[country]['city_coordinates'][0])
        lon = float(main_dict[country]['city_coordinates'][1])
        min_lat, max_lat = lat - 0.25, lat + 0.25
        min_lon, max_lon = lon - 0.25, lon + 0.25
        lat1 = round(random.uniform(min_lat, max_lat), 4)
        lon1 = round(random.uniform(min_lon, max_lon), 4)
        lats.append(lat1)
        lons.append(lon1)
    print("Lats/lons: ", len(lats), len(lons))
    return lats, lons


total_agents = 0
countries = []
cities = []
fakers = []
for k, v in main_dict.items():
    countries.append(k)
    total_agents += v['number_of_agents']
    cities.append(v['city'])
    fakers.append(Faker(v['faker_abbriv']))


with open('nicknames_str.txt', 'r') as f:
    nicknames = [i.capitalize() for i in f.read().split()]
nicknames_unique = list(set(nicknames))
nicknames = nicknames_unique + \
                            [None for i in range(total_agents - len(nicknames))]
random.shuffle(nicknames)


column_names = ['name', 'alias', 'address', 'city', 'country',
                'lat', 'lon', 'code_phrase']


def generate_profile(regional_faker, country):
    """
    Creates a df of criminals with columns:
    name
    nickname
    address
    city
    country
    lat
    lon
    code_phrase

    """

    n_agents = main_dict[country]['number_of_agents']
    name_col = [regional_faker.name() for i in range(n_agents)]
    nicknames_col = [random.choice(nicknames) for i in range(
        n_agents)]
    address_col = [regional_faker.address().replace('\n', ' ') for i in
                   range(n_agents)]
    city_col = [main_dict[country]['city'] for i in range(n_agents)]
    country_col = [country for i in range(n_agents)]
    lats_col, lons_col = generate_lat_lon(country)
    code_phrase_col = [" ".join(faker_en.words()[0:2]) for i in range(
        n_agents)]

    cols_data = [name_col, nicknames_col, address_col, city_col, country_col,
            lats_col, lons_col, code_phrase_col]

    # generate dict to create a df later
    regional_dict = {}
    for column_name, data_list in zip(column_names, cols_data):
        regional_dict[column_name] = data_list
    df = pd.DataFrame(regional_dict)
    df = df.astype(str)


    return df

def add_accomplices():
    """
    creates a df for three criminals (accomplices of Moriarty
    """
    mike_mulv = pd.DataFrame({'name': 'Michael Mullie', 'alias': 'Blunt',
                              'address': "",
                              'city': 'London', 'country': 'United Kingdom',
                              'lat': '51.523756', 'lon': '-0.158349',
                              'code_phrase': 'beij mast'}, index=[0])

    rude_jully = pd.DataFrame({'name': 'Ruddie Jully', 'alias': 'Rude',
                               'city': 'London', 'country': 'United Kingdom',
                               'lat': '51.523756', 'lon': '-0.158349',
                               'code_phrase': 'fuj muster'}, index=[0])

    gore_sondy = pd.DataFrame({'name': 'Gore Sondy', 'alias': 'Lux',
                               'city': 'London', 'country': 'United Kingdom',
                               'lat': '51.523756', 'lon': '-0.158349',
                               'code_phrase': 'taj mongol'}, index=[0])

    df = pd.concat([mike_mulv, rude_jully, gore_sondy], sort=False,
                   ignore_index=False)
    df = df.astype(str)
    print(df.dtypes)

    return df


profile_dfs = []
for f, c in zip(fakers, countries):
    profile_dfs.append(generate_profile(f, c))
print("N profiles: ", len(profile_dfs))

df_accomplices = add_accomplices()
profile_dfs.append(df_accomplices)
full_df = pd.concat(profile_dfs, ignore_index=True, sort=False)
# full_df = pd.concat([full_df, df_accomplices],ignore_index=True, sort=False)
print("Types: ")
print(full_df.dtypes)

full_df.to_csv('main_table_with_3.csv', header=True, index=False)
# country_df = generate_profile(faker_fr, 'France')
# print(full_df.shape)
# print(full_df.iloc[0:5, :])
