
import pandas as pd

from faker import Faker
# from helpers import seed
seed = 1234
Faker.seed(seed)
faker = Faker()


def test_generate_aliases():
    """"""
    from generate_data_files import generate_aliases

    # create mock df for testing a column
    temp_df = pd.DataFrame({'name': ['Ann', 'Bob', 'Cat', 'Don']})

    df_out = generate_aliases(temp_df, 1)

    assert df_out.shape[0] > 0, "data frame should not be empty"
    assert 'alias' in df_out.columns, "alias column must be present"
    assert sum(df_out["alias"].isna()) < df_out.shape[0], "all aliases can't be null"


def test_generate_country_criminals_df():

    from generate_data_files import generate_country_criminals_df

    df_out = generate_country_criminals_df(Faker('fr_FR'), 'France')
    assert df_out.shape[0] > 0, "data frame should not be empty"
    assert len(df_out.columns) == 7, "data frame should have 7 columns. Found: {}".format(len(df_out.shape[0]))

    assert set(df_out.columns) == set(['name', 'id', 'address', 'lat', 'lon', 'country', 'city']), \
            "column names are incorrect. Expected: 'name', 'id', 'address', 'lat', 'lon', 'country', 'city'"


def test_parse_main_dict():

    from generate_data_files import parse_main_dict

    result = parse_main_dict()

    assert isinstance(result, tuple), "output must be a tuple"
    assert len(result) == 4, "incorrect number of items in tuple. expected: 4, got: {}".format(len(result))


def test_add_date_weekday_column():

    from generate_data_files import add_date_weekday_column

    # create mock df for testing a column
    temp_df = pd.DataFrame({'name': ['Ann', 'Bob', 'Cat', 'Don']})
    df_out = add_date_weekday_column(temp_df)

    assert df_out.shape[0] > 0, "data frame should not be empty"
    assert 'date' in df_out.columns, "date column must be present"
    assert 'weekday' in df_out.columns, "alias column must be present"


def test_add_crime_types():

    from generate_data_files import add_crime_types

    # create mock df for testing a column
    temp_df = pd.DataFrame({'name': ['Ann', 'Bob', 'Cat', 'Don']})

    df_out = add_crime_types(temp_df)
    assert df_out.shape[0] > 0, "data frame should not be empty"
    assert 'crime_type' in df_out.columns, "crime_type column must be present"


def test_generate_df_with_criminals():

    from generate_data_files import generate_df_with_criminals
    from generate_data_files import identify_moriarty

    # generate the df
    df_out = generate_df_with_criminals()

    assert df_out.shape[0] > 0, "data frame should not be empty"
    assert len(df_out.columns) == 12, "data frame should have 12 columns. Found: {}".format(len(df_out.shape[0]))
    assert set(df_out.columns) == set(['name', 'alias', 'id', 'address', 'lat', 'lon', 'country',
             'city', 'date', 'crime_type', 'profit', 'weekday']),  \
        """incorrect columns. expected: ['name', 'alias', 'id', 'address', 'lat', 'lon', 'country',
             'city', 'date', 'crime_type', 'profit', 'weekday'], got: {}""".format(df_out.columns)

    # check that using the generated 'df_out' Moriarty's name is correct
    moriarty_name = identify_moriarty(df_out, seed, save=False)

    assert moriarty_name == 'Gabriel Le Schneider',  \
        """Moriarty name should be Gabriel Le Schneider for seed 1234. 
            Got: {} for seed {}""".format(moriarty_name, seed)
