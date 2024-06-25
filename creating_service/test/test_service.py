import numpy as np

def test_model(previous_close, close, coefficients, intercept):
    X = np.array(previous_close).reshape(-1, 1)
    y = np.array(close)
    
    predictions = intercept + np.array(coefficients)[0] * X.flatten()
    rmse = np.sqrt(np.mean((y - predictions) ** 2))
    
    return predictions.tolist(), rmse
