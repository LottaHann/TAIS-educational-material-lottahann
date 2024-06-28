import pandas as pd
from sklearn.model_selection import train_test_split


def clean_data(csv_file):
    data = pd.read_csv(csv_file)
    data['Date'] = pd.to_datetime(data['Date'])
    data['Previous_Close'] = data['Close'].shift(1)
    data = data.dropna()
    
    x = data[['Previous_Close']]
    y = data['Close']
    dates = data['Date']
    
    x_train, x_test, y_train, y_test, dates_train, dates_test = train_test_split(
        x, y, dates, test_size=0.2, shuffle=False
    )
    
    # Flatten the lists
    x_train_flat = [item for sublist in x_train.values for item in sublist]
    x_test_flat = [item for sublist in x_test.values for item in sublist]
    y_train_flat = y_train.tolist()
    y_test_flat = y_test.tolist()
    dates_train_str = dates_train.dt.strftime('%Y-%m-%d').tolist()
    dates_test_str = dates_test.dt.strftime('%Y-%m-%d').tolist()
    
    return x_train_flat, x_test_flat, y_train_flat, y_test_flat, dates_train_str, dates_test_str
