import pandas as pd
import os
from pathlib import Path

def get_case_query():
    return Path('movies_api/rest_api/etl/case_query.sql').read_text()

def get_database_creation_query():
    return Path('movies_api/database/field schema.sql').read_text()

def initialize_data():
    df = None
    for csv in list_csv():
        if df is None:
            df = load_csv(csv)
        else:
            df.append(load_csv(csv),ignore_index=True)    
    return df

    
def filter_rows_by_values(df, col, values):
    df= df[~df[col].isin(values)]
    df.dropna(subset=col,how='all',inplace=True)
    return df

def load_csv(file_path):
    columns = []
    columns_validation = ['year','title','studios','producers','winner']
    with open(file_path) as f:
        line = f.readline().replace("\n", '')
        columns = line.split(";")
    if  set(columns_validation) != set(columns):
        raise Exception(f'CSV headers not match, should have: {columns_validation}, the given header is: {columns}')
    df = pd.read_csv(file_path, sep=';', names=columns,
                        on_bad_lines='warn')
    df = filter_rows_by_values(df,columns,columns)      
    df["year"] = pd.to_numeric(df["year"], errors='raise')
    return df

def list_csv():
    file_list = os.listdir('movies_api/csv')
    available_csv = []
    for file in file_list:
        if file.endswith('.csv'):
            available_csv.append(f'movies_api/csv/{file}')
    return available_csv

    
