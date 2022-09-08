import pandas as pd
import os


def initialize_data():
    
    def filter_rows_by_values(df, col, values):
        df= df[~df[col].isin(values)]
        df.dropna(subset=col,how='all',inplace=True)
        return df

    def load_csv(file_path):
        columns = []
        with open(file_path) as f:
            line = f.readline().replace("\n", '')
            columns = line.split(";")
        df = pd.read_csv(file_path, sep=';', names=columns,
                         on_bad_lines='warn')
        df = filter_rows_by_values(df,columns,columns)        

        return df

    def list_csv():
        file_list = os.listdir('movies_api/csv')
        available_csv = []
        for file in file_list:
            if file.endswith('.csv'):
                available_csv.append(f'movies_api/csv/{file}')

        return available_csv

    df = None
    for csv in list_csv():
        if df is None:
            df = load_csv(csv)
        else:
            df.append(load_csv(csv),ignore_index=True)
    
    return df

