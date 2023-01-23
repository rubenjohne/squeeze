import os
import yfinance as yf

# delete all files in the folder 
dir = "datasets"
for f in os.listdir(dir):
   os.remove(os.path.join(dir, f))

#with open('stocks.csv') as f:
with open('bensdorp.csv') as f:
  
    lines = f.read().splitlines()
    for symbol in lines:
            # if the file already exists skip it 
            if os.path.isfile("datasets/{}.csv".format(symbol)):
                continue
            print(symbol)
            data = yf.download(symbol, start="2022-01-01", end="2022-12-13")
            data.to_csv("datasets/{}.csv".format(symbol))

# TESTER TO DOWNLOAD 1 SYMBOL 
# symbol = 'AAPL'
# print(symbol)
# data = yf.download(symbol, start="2021-03-01", end="2021-08-31")
# data.to_csv("datasets/{}.csv".format(symbol))

print("DONE")