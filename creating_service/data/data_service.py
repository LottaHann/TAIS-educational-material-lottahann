import pandas as pd

def clean_data(csv_file):
    data = pd.read_csv(csv_file)
    data['Date'] = pd.to_datetime(data['Date'])
    data['Previous_Close'] = data['Close'].shift(1)
    data = data.dropna()
    return data['Previous_Close'].tolist(), data['Close'].tolist(), data['Date'].astype(str).tolist()
