import numpy as np
from sklearn.linear_model import LinearRegression

def train_model(previous_close, close):
    X = np.array(previous_close).reshape(-1, 1)
    y = np.array(close)
    
    model = LinearRegression()
    model.fit(X, y)
    
    predictions = model.predict(X)
    rmse = np.sqrt(np.mean((y - predictions) ** 2))
    
    return model.coef_.tolist(), model.intercept_, rmse
