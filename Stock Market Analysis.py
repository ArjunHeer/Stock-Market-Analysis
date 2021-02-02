import numpy as np 
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import pandas_datareader.data as web
from pandas.plotting import scatter_matrix
from mplfinance.original_flavor import candlestick_ohlc
from matplotlib.dates import DateFormatter, WeekdayLocator, DayLocator, MONDAY


start = datetime.datetime.now() - datetime.timedelta(6*365)
end = datetime.datetime.now()

tesla = web.DataReader("TSLA", "yahoo", start, end)
ford = web.DataReader("ford", "yahoo", start, end)
gm = web.DataReader("gm", "yahoo", start, end)

# print(tesla.head())
# print(ford.head())
# print(gm.head())


# tesla.to_csv ('Tesla_stock.csv')
# ford.to_csv ('ford_stock.csv')
# gm.to_csv ('gm_stock.csv')


tesla['Open'].plot(label='Tesla', figsize=(15, 7))
ford['Open'].plot(label='ford')
gm['Open'].plot(label='gm')

plt.legend()
plt.title("Stock prices")
plt.ylabel("Stock Price")

plt.show()

tesla['Volume'].plot(label='Tesla', figsize=(15, 7))
ford['Volume'].plot(label='ford')
gm['Volume'].plot(label='gm')

plt.legend()
plt.title("Volume traded")
plt.ylabel("Volume traded")

plt.show()

# print(ford.iloc[[ford['Volume'].argmax()]])
# ford.iloc[470:520]['Open'].plot()
plt.show()

tesla['Total Traded'] = tesla['Open'] * tesla['Volume']
ford['Total Traded'] = ford['Open'] * ford['Volume']
gm['Total Traded'] = gm['Open'] * gm['Volume']

# print(tesla.head())
# print(ford.head())
# print(gm.head())


tesla['Total Traded'].plot(label='Tesla', figsize=(15, 7))
ford['Total Traded'].plot(label='ford')
gm['Total Traded'].plot(label='gm', figsize=(15, 7))

plt.legend()
plt.title("Total traded")
plt.ylabel("Total traded")
plt.show()

# print(tesla['Total Traded'].argmax())
# print(tesla.iloc[tesla['Total Traded'].argmax()])

gm['Open'].plot(figsize=(15, 7))

## MOVING AVG - remove noise - if too high can miss trends
gm['MA50'] = gm['Open'].rolling(50).mean()
gm['MA50'].plot(label='MA50')

gm['MA100'] = gm['Open'].rolling(100).mean()
gm['MA100'].plot(label='MA100')

plt.legend()

plt.show()

## Correlation 

car_comp = pd.concat([tesla['Open'], ford['Open'], gm['Open']], axis=1)
car_comp.columns = ['Tesla Open', 'Ford Open', 'GM Open']

scatter_matrix(car_comp, figsize=(8, 8), hist_kwds={'bins': 50})
# plt.show()


# ford_reset = ford.loc['2012-01':'2012-01'].reset_index()

# ford_reset['date_ax'] = ford_reset['Date'].apply(lambda date: date2num(date))
# ford_values = [tuple(vals) for vals in 
# 	ford_reset[['date_ax', 'Open','High', 'Low', 'Close']].values]

# mondays = WeekdayLocator(MONDAY)
# alldays = DayLocator()
# weekFormatter = DateFormatter('%b %d')
# dayFormatter = DateFormatter('%d')

# fig, ax = plt.subplots()
# candlestick_ohlc(ax, ford_values, colorup='g', colordown='r')

# plt.show() 

# Daily % change 
# r(t) = p(t)/p(t-1) - 1

tesla['returns'] = (tesla['Close']/tesla['Close'].shift(1)) - 1
ford['returns'] = (ford['Close']/ford['Close'].shift(1)) - 1
gm['returns'] = (gm['Close']/gm['Close'].shift(1)) - 1

tesla['returns'].hist(bins=50, label='tesla', alpha=0.5, figsize=(13, 6))
ford['returns'].hist(bins=50, label='ford', alpha=0.5)
gm['returns'].hist(bins=50, label='gm', alpha=0.5)

plt.show()

tesla['returns'].plot(kind='kde', label='tesla', figsize=(15,6))
ford['returns'].plot(kind='kde', label='ford')
gm['returns'].plot(kind='kde', label='gm')

plt.legend()

plt.show()

box_df = pd.concat([tesla['returns'], gm['returns'], ford['returns']], axis=1)
box_df.columns=['tesla', 'ford', 'gm']
box_df.plot(kind='box', figsize=(16, 6))

plt.show()

scatter_matrix(box_df, figsize=(8,8), hist_kwds={'bins':50}, alpha=0.25)
plt.show()

## Cumulative return
# i(t) = (1 + r(t)) * i(t-1)  --> u can plug it in to other formula with p(t)

tesla['Cumulative returns'] = (1 + tesla['returns']).cumprod()
ford['Cumulative returns'] = (1 + ford['returns']).cumprod()
gm['Cumulative returns'] = (1 + gm['returns']).cumprod()

tesla['Cumulative returns'].plot(label='tesla', figsize=(15,7))
ford['Cumulative returns'].plot(label='ford')
gm['Cumulative returns'].plot(label='gm')

plt.legend()
plt.show()

