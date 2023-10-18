# Importing Packages

import pandas as pd
import numpy as np
import psycopg2
import argparse
from sqlalchemy import create_engine

# extracting the data from source
def extract_data(source):
    return pd.read_csv(source)

# Performing the data transformations
def transform_data(data):
    new_data = data.copy()
    # Converting all the column names to lower case, replacing the spaces with underscores
    new_data.columns = new_data.columns.str.lower().str.replace(' ', '_')
    # dropping duplicates within the primary key
    new_data = new_data.drop_duplicates(subset=['animal_id'])
    # converting into datetime column into specific format
    new_data['datetime'] = pd.to_datetime(new_data['datetime'], format='%m/%d/%Y %I:%M:%S %p')
    # splitting the monthyear column into month and year columns
    new_data[['month','year']] = new_data.monthyear.str.split(' ', expand = True)
    # filling the null values with the name "Unkown"
    new_data['sex'] = new_data['sex_upon_outcome'].replace('Unkown', np.nan)
    new_data.drop(columns = ['monthyear', 'sex_upon_outcome'], inplace = True)
    print(new_data.columns)
    return new_data

def load_data(data):
    # creating the dimension tables from the main dataframe
    dim_animal = data[['animal_id','name','date_of_birth','animal_type','breed','color']]
    dim_time = data[['datetime','month','year']]
    dim_time['date_id'] = dim_time.index + 1
    dim_outcometype = data[['outcome_type','outcome_subtype']]
    dim_outcometype['outcome_id'] = dim_outcometype.index + 1

    
    # Merge the dim_animal, dim_time, and dim_outcometype DataFrames to create the fact table
    fct_animal = pd.merge(dim_animal, dim_time, left_index=True, right_index=True)
    fct_animal = pd.merge(fct_animal, dim_outcometype, left_index=True, right_index=True)

    # Define the primary key for the fact table (breed_id)
    fct_animal['breed_id'] = fct_animal.index + 1

    # Reorder the columns to match the table structure
    fct_animal = fct_animal[['breed_id', 'animal_id', 'date_id', 'outcome_id', 'month', 'year', 'outcome_type']]

    # database connection
    db_url = "postgresql+psycopg2://vamsigontu:Ramsita123@database:5432/shelter"
    conn = create_engine(db_url)

    # Converting the above created dataframes to tables 
    data.to_sql("outcomes", conn, if_exists = "append", index = False)
    dim_animal.to_sql("dim_animal", conn, if_exists = "append", index = False)
    dim_time.to_sql("dim_time", conn, if_exists = "append", index = False)
    dim_outcometype.to_sql("dim_outcometype", conn, if_exists = "append", index = False)
    fct_animal.to_sql("fct_animal", conn, if_exists = "append", index = False)
    print("Tables Creation Complete")
# Main pipeline

if __name__ == "__main__":
    parser =  argparse.ArgumentParser()
    parser.add_argument('source', help = 'source csv')
    # parser.add_argument('target', help = 'target csv')
    args = parser.parse_args()

    print("Starting...")
    df = extract_data(args.source)
    new_df = transform_data(df)
    load_data(new_df)
    print("complete")
