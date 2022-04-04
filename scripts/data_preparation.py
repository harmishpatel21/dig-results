import pandas as pd
import os

def read_data(path):
    df = pd.read_csv(path)
    return df

def export_data(df, string):
    path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    # filename = f'{path}/{str(uploaded_file["name"].split(".")[0])}_export.csv'
    filename = f'{path}/{string}.csv'
    df.to_csv(filename, index=False)
    return None

def filter_data(df, col, val):
    return df[df[col] == val]

def clean_data(df):
    for i in df.columns:
        if '%' in i:
            df[i] = df[i].apply(lambda x: int(str(x).replace('%', '')) if '%' in str(x) else x)
    return df