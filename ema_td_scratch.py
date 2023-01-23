import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

datafile = 'data_td.csv'

data = pd.read_csv(datafile, index_col='Date')
data.index = pd.to_datetime(data.index)

weights = np.arange(1,11) #this creates an array with integers 1 to 10 included
wma10 = data['Price'].rolling(10).apply(lambda prices: np.dot(prices, weights)/weights.sum(), raw=True)
data['10-day WMA'] = wma10

# print(wma10.head(20))

data['Our 10-day WMA'] = np.round(wma10, decimals=3)
# print(data[['Price', '10-day WMA', 'Our 10-day WMA']].head(20))

ema10 = data['Price'].ewm(span=10, adjust=False).mean()
print(np.round(ema10, decimals=2))