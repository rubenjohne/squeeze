import os
import pandas as pd
import pandas_datareader
import matplotlib.pyplot as plt
import numpy as np
from datetime import date

symbols = ['AAPL']
csv_df = pd.DataFrame(columns=['stock'])
csv_df_bear = pd.DataFrame(columns=['stock'])
today = date.today()

# loop through the SP500 stock tickers 
for filename in os.listdir('datasets'):
    #print(filename)
    symbol = filename.split(".")[0]
    #print(symbol)
    df = pd.read_csv('datasets/{}'.format(filename), encoding='latin-1')
    if df.empty:
        continue
    
    # create the columns for ema 50, 21, 14
    df['ema50'] = np.round(df['Close'].ewm(span=50).mean(), decimals=2)
    df['ema21'] = np.round(df['Close'].ewm(span=21).mean(), decimals=2)
    df['ema14'] = np.round(df['Close'].ewm(span=14).mean(), decimals=2)


    # if symbol in symbols:
    #     print(df)

    # BULLISH find the ema that the 14 is less than 21 yesterday and tomorrow the 14 is greater than 21 
    if (df.iloc[-2]['ema14'] < df.iloc[-2]['ema21']) and (df.iloc[-1]['ema14'] > df.iloc[-1]['ema21'] and df.iloc[-1]['Close'] > df.iloc[-1]['ema50']) :
    #if (df.iloc[-2]['ema14'] < df.iloc[-2]['ema21']) and (df.iloc[-1]['ema14'] > df.iloc[-1]['ema21']) :
         print("{} turned bullish on positional ema {}".format(symbol, df.iloc[-1]['Date']))
         csv_df = csv_df.append({'stock': symbol}, ignore_index=True)


    # BEARISH find the ema that the 14 is greater than 21 yesterday and tomorrow the 14 is less than 21 
    if (df.iloc[-2]['ema14'] > df.iloc[-2]['ema21']) and (df.iloc[-1]['ema14'] < df.iloc[-1]['ema21'] and df.iloc[-1]['Close'] < df.iloc[-1]['ema50']):
    #if (df.iloc[-2]['ema14'] > df.iloc[-2]['ema21']) and (df.iloc[-1]['ema14'] < df.iloc[-1]['ema21']):
         print("{} turned bearish on positional ema {}".format(symbol, df.iloc[-1]['Date']))
         csv_df_bear = csv_df_bear.append({'stock': symbol}, ignore_index=True)
    
    #df.to_csv(symbol + '.csv', index=False, header=True)


csv_df.to_csv('Bullish-' + str(today) + '.csv' , index=False, header=False)
csv_df_bear.to_csv('Bearish-' + str(today) + '.csv', index=False, header=False)