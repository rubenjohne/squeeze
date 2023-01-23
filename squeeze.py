import os, pandas
import plotly.graph_objects as go
from datetime import date


symbols = ['AAPL']
# create empty dataframe to add stocks to export as csv 
csv_df = pandas.DataFrame(columns=['stock'])
csv_out_df = pandas.DataFrame(columns=['stock'])
csv_bb_df = pandas.DataFrame(columns=['stock'])
today = date.today()

# function to append stock to csv_df 
def append_stock(symbol):
    csv_df.append({'stock': symbol}, ignore_index=True)
    return

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

    def out_upper_bb(df):
        return df['Close'] > df['upper_band']


    df['squeeze_on'] = df.apply(in_squeeze, axis=1)
    # breaking out touched upper bollinger band 
    df['upper_bb_breakout'] = df.apply(out_upper_bb, axis=1)

    # coming out of the squueeze
    if df.iloc[-2]['squeeze_on'] and not df.iloc[-1]['squeeze_on']:
         print("{} is coming out the squeeze on {}".format(symbol, df.iloc[-1]['Date']))
         # append stocks here to csv df 
         csv_out_df = csv_out_df.append({'stock': symbol}, ignore_index=True)


    # in the squeeze 
    if df.iloc[-1]['squeeze_on']:
        print("{} is in the squeeze".format(symbol))
        # append stocks here to csv df 
        csv_df = csv_df.append({'stock': symbol}, ignore_index=True)


    # bollinger band breakout
    if df.iloc[-1]['upper_bb_breakout'] and not df.iloc[-2]['upper_bb_breakout']:
        print("{} is breaking out of the bolinger band".format(symbol, df.iloc[-1]['Date']))
        csv_bb_df = csv_bb_df.append({'stock': symbol}, ignore_index=True)

    
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

csv_df.to_csv('squeeze-'  + str(today) + '.csv', index=False, header=False)
csv_out_df.to_csv('out_squeeze-'  + str(today) + '.csv', index=False, header=False)
csv_bb_df.to_csv('BB-'  + str(today) + '.csv', index=False, header=False)