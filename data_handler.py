import pandas as pd

def load_excel(file_path):
    df = pd.read_excel(file_path)
    df.columns = df.columns.str.strip()
    return df

def get_full_data_as_text(df):
    return df.to_string(index = False)