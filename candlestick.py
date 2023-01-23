import talib
import yfinance as yf
import pandas as pd
import os
from datetime import date

#data = yf.download("SPY", start="2021-11-01", end="2021-11-30")

#print(data['Close'][-1])

#engulfing = talib.CDLENGULFING(data['Open'], data['High'], data['Low'], data['Close'])

#data['engulfing'] = engulfing

today = date.today()

csv_df = pd.DataFrame(columns=['stock'])
csv_evening_df = pd.DataFrame(columns=['stock'])
csv_morning_df = pd.DataFrame(columns=['stock'])
csv_candlepick_df = pd.DataFrame(columns=['stock'])

for filename in os.listdir('datasets'):
    symbol = filename.split(".")[0]
    data = pd.read_csv('datasets/{}'.format(filename))
    if data.empty:
        continue

    # create engulfing column 
    engulfing = talib.CDLENGULFING(data['Open'], data['High'], data['Low'], data['Close'])
    data['Engulfing'] = engulfing

    # create evening start colum 
    evening_star = talib.CDLEVENINGSTAR(data['Open'], data['High'], data['Low'], data['Close'])
    data['Evening Star'] = evening_star

    # create morning star column
    morning_star = talib.CDLMORNINGSTAR(data['Open'], data['High'], data['Low'], data['Close'])
    data['Morning Star'] = morning_star

 
    # create generic candle pick column
    candle_pick = talib.CDLABANDONEDBABY(data['Open'], data['High'], data['Low'], data['Close'])
    data['Candle Pick'] = candle_pick
    
    # check if the last day is engulfing 
    if (data.iloc[-1]['Engulfing']!= 0):
        csv_df = csv_df.append({'stock': symbol}, ignore_index=True)
        print("{} is showing engulfing pattern {}".format(symbol, data.iloc[-1]['Date']))

    # check if the last day is evening star  
    if (data.iloc[-1]['Evening Star']!= 0):
        csv_evening_df = csv_evening_df.append({'stock': symbol}, ignore_index=True)
        print("{} is showing evening star pattern {}".format(symbol, data.iloc[-1]['Date']))

    # check if the last day is morning star  
    if (data.iloc[-1]['Morning Star']!= 0):
        csv_morning_df = csv_morning_df.append({'stock': symbol}, ignore_index=True)
        print("{} is showing morning star pattern {}".format(symbol, data.iloc[-1]['Date']))


    # check if the last day is morning star  
    if (data.iloc[-1]['Candle Pick']!= 0):
        csv_candlepick_df = csv_candlepick_df.append({'stock': symbol}, ignore_index=True)
        print("{} is showing candle pick pattern {}".format(symbol, data.iloc[-1]['Date']))

csv_df.to_csv('engulfing-'  + str(today) + '.csv', index=False, header=False)
csv_evening_df.to_csv('evening_star-'  + str(today) + '.csv', index=False, header=False)
csv_morning_df.to_csv('morning_star-'  + str(today) + '.csv', index=False, header=False)
csv_candlepick_df.to_csv('candle_pick-'  + str(today) + '.csv', index=False, header=False)