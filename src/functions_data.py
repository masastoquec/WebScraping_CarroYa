import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from ydata_profiling import ProfileReport


## Cleaning functions

def standarize_column_names(df:pd.DataFrame) -> pd.DataFrame:
    """ Standarize column names in a DataFrame"""
    df.columns =    df.columns.str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')\
                    .str.replace('.','').str.replace('/','_').str.replace('-','_').str.replace('__','_')\
                    .str.replace('á','a').str.replace('é','e').str.replace('í','i').str.replace('ó','o').str.replace('ú','u')
    df = df.loc[:, ~df.columns.str.contains('unnamed')]
    return df

# Define function to clean and preprocess DataFrame
def clean_dataframe(df:pd.DataFrame, schema:dict, missing_columns_check:list) -> pd.DataFrame:
    print(f'df original size: {df.shape} - columns: {df.columns}' )
    # Standarize column names
    df = standarize_column_names(df)
    # Remove duplicates
    df = df.drop_duplicates()
    # Handle missing values
    df = df.dropna(subset=missing_columns_check)

    # Format fields to match the schema
    for column, dtype in schema.items():
        if column in df.columns:
            if dtype == 'date' and df[column].dtype != 'datetime64[ns]':
                df[column] = pd.to_datetime(df[column])
            elif dtype == 'int' and df[column].dtype != 'int64':
                df[column] = df[column].astype('int')
            elif dtype == 'double' and df[column].dtype != 'float64':
                df[column] = df[column].str.replace('$','').str.replace('.','').str.replace(',','').str.replace(' km','').str.replace(' ','').astype('float')
            elif dtype == 'string' and df[column].dtype != 'object':
                df[column] = df[column].astype('str')
            elif dtype == 'category':
                df[column] = df[column].str.lower().str.replace('(', '').str.replace(')', '')\
                    .str.replace('.','').str.replace('/','_').str.replace('-','_').str.replace('__','_')\
                    .str.replace('á','a').str.replace('é','e').str.replace('í','i').str.replace('ó','o').str.replace('ú','u').astype('category')
    print(f'df cleaned size: {df.shape} - columns: {df.columns}' )
    return df
