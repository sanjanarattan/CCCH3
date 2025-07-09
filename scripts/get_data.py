import json
import urllib.request
import pandas as pd
import sqlite3


# api call
def api(url, limit=100):
    offset = 0
    all_records = []

    while True:
        full_url = f"{url}&limit={limit}&offset={offset}"
        with urllib.request.urlopen(full_url) as fileobj:
            response_dict = json.loads(fileobj.read())

        records = response_dict['result']['records']
        if not records:
            break

        all_records.extend(records)
        offset += limit

    return pd.DataFrame.from_records(all_records)

# filter ccc coc data
def filterDf(df):
    return df[df['LOCATION_ID'] == 'CA-505']

# create dataframes
race_df = filterDf(api('https://data.ca.gov/api/3/action/datastore_search?resource_id=b7ce1242-0e33-44c8-b561-4c34c5e78312'))
age_df = filterDf(api('https://data.ca.gov/api/3/action/datastore_search?resource_id=b1a5ae24-5842-425c-b56c-aa90f8f1c767'))
vet_df = filterDf(api('https://data.ca.gov/api/3/action/datastore_search?resource_id=90731a7d-3e33-4d45-9bde-1b0fd65c51cb'))
disab_df = filterDf(api('https://data.ca.gov/api/3/action/datastore_search?resource_id=15c6f222-56d9-4184-97cd-fca6923f2474'))
gender_df = filterDf(api('https://data.ca.gov/api/3/action/datastore_search?resource_id=57142555-f2da-462f-a999-d44abf0af69c'))

# check dataframes
print(race_df.head())
print(age_df.head())
print(vet_df.head())
print(disab_df.head())
print(gender_df.head())

# connect to db
conn = sqlite3.connect('ccc_homelessness.db')

def to_table(df, name):
    df.to_sql(f'{name}', conn, if_exists='replace')

to_table(race_df, "race")
to_table(age_df, "age")
to_table(vet_df, "veteran")
to_table(disab_df, "disabled")
to_table(gender_df, "gender")

# check sqldb
for attr in ["race", "gender", "age", "veteran", "disabled"]:
    df = pd.read_sql(f'SELECT * FROM {attr} LIMIT 5', conn)
    print(df.head())

