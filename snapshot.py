import os
import yfinance as yf

with open('symbols.csv') as f:

    lines = f.read().splitlines()
    for symbol in lines:
            # if the file already exists skip it 
            if os.path.isfile("datasets/{}.csv".format(symbol)):
                continue
            print(symbol)
            data = yf.download(symbol, start="2021-02-01", end="2021-08-20")
            data.to_csv("datasets/{}.csv".format(symbol))

print("DONE")