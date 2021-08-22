import os, pandas
import plotly.graph_objects as go
from datetime import datetime


symbols = ['AAPL']

for filename in os.listdir('datasets'):
    #print(filename)
    symbol = filename.split(".")[0]
    # print(symbol)
    df = pandas.read_csv('datasets/{}'.format(filename))
    if df.empty:
        continue

    df['20sma'] = df['Close'].rolling(window=20).mean()
    df['stddev'] = df['Close'].rolling(window=20).std()
    df['lower_band'] = df['20sma'] - (2* df['stddev'])
    df['upper_band'] = df['20sma'] + (2 * df['stddev'])

    df['TR'] = abs(df['High'] - df['Low'])
    df['ATR'] = df['TR'].rolling(window=20).mean()

    df['lower_keltner'] = df['20sma'] - (df['ATR'] * 1.5)
    df['upper_keltner'] = df['20sma'] + (df['ATR'] * 1.5)

    def in_squeeze(df):
        return df['lower_band'] > df['lower_keltner'] and df['upper_band'] < df['upper_keltner']

    df['squeeze_on'] = df.apply(in_squeeze, axis=1)

    # coming out of the squueeze
    if df.iloc[-6]['squeeze_on'] and not df.iloc[-5]['squeeze_on']:
         print("{} is coming out the squeeze on {}".format(symbol, df.iloc[-5]['Date']))

    # in the squeeze 
    # if df.iloc[-1]['squeeze_on']:
    #     print("{} is in the squeeze".format(symbol))

    # if symbol in symbols:
    #     print(df)
    #     aapl_df = df 

# candlestick = go.Candlestick(x=aapl_df['Date'],
#                 open=aapl_df['Open'],
#                 high=aapl_df['High'],
#                 low=aapl_df['Low'],
#                 close=aapl_df['Close'])
# upper_band = go.Scatter(x=aapl_df['Date'], y=aapl_df['upper_band'], name='Upper Bollinger Band', line={'color' : 'red'})
# lower_band = go.Scatter(x=aapl_df['Date'], y=aapl_df['lower_band'], name='Lower Bollinger Band', line={'color': 'red'})
# upper_keltner = go.Scatter(x=aapl_df['Date'], y=aapl_df['upper_keltner'], name='Upper Keltner Channel', line={'color' : 'orange'})
# lower_keltner = go.Scatter(x=aapl_df['Date'], y=aapl_df['lower_keltner'], name='Lower Keltner Channel', line={'color': 'orange'})

# sma_20 = go.Scatter(x=aapl_df['Date'], y=aapl_df['20sma'], name='20 SMA', line={'color' : 'blue'})

# fig = go.Figure(data=[candlestick, upper_band, lower_band, sma_20, upper_keltner, lower_keltner])
# fig.layout.xaxis.type = 'category'
# fig.layout.xaxis.rangeslider.visible = False

# fig.show()