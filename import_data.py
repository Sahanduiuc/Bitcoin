#https://github.com/sammchardy/python-binance
api_key = ''
api_secret = ''

import time
import datetime
import pandas as pd
import numpy as np
from binance.client import Client
#Connect to Binance: 
client = Client(api_key, api_secret)

#Returns historical trades bid/ask for the last 24 hrs (1 minute interval)
def generateOHLC(ticker): 
	klines = client.get_historical_klines(ticker, Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")
	ohlc = pd.DataFrame({'open_time': [float(klines[i][0]) for i in range(len(klines))],
						 'open': [float(klines[i][1]) for i in range(len(klines))],
						 'high': [float(klines[i][2]) for i in range(len(klines))],
						 'low': [float(klines[i][3]) for i in range(len(klines))],
						 'close': [float(klines[i][4]) for i in range(len(klines))],
						 'volume': [float(klines[i][5]) for i in range(len(klines))],
						 'close_time': [float(klines[i][6]) for i in range(len(klines))],
						 'num_trades': [float(klines[i][7]) for i in range(len(klines))]})
	#Price refers to midpoint price, defined as --> (high + low)/ 2
	ohlc['price'] = (ohlc['high'] + ohlc['low'])/2
	return(ohlc)

#Can change base_currency to be USD, ETH, etc. for other coins; default to BTC
def returnTickers(base_currency = "BTC"):
	data = client.get_all_tickers()
	return [data[i]['symbol']for i in range(len(data)) if data[i]['symbol'][3:] == base_currency]


#    KLINE_INTERVAL_1MINUTE = '1m'
#    KLINE_INTERVAL_3MINUTE = '3m'
#    KLINE_INTERVAL_5MINUTE = '5m'
#    KLINE_INTERVAL_15MINUTE = '15m'
#    KLINE_INTERVAL_30MINUTE = '30m'
#    KLINE_INTERVAL_1HOUR = '1h'
#    KLINE_INTERVAL_2HOUR = '2h'
#    KLINE_INTERVAL_4HOUR = '4h'
#    KLINE_INTERVAL_6HOUR = '6h'
#    KLINE_INTERVAL_8HOUR = '8h'
#    KLINE_INTERVAL_12HOUR = '12h'
#    KLINE_INTERVAL_1DAY = '1d'
#    KLINE_INTERVAL_3DAY = '3d'
#    KLINE_INTERVAL_1WEEK = '1w'
#    KLINE_INTERVAL_1MONTH = '1M'
#Date in format of day, month, year --> i.e. 1 Dec, 2017
def generateHistoricalData(ticker, start, end, period = 30):
	if period == 30: 
		pull_type = Client.KLINE_INTERVAL_30MINUTE
	if period == 1: 
		pull_type = Client.KLINE_INTERVAL_1MINUTE 
	if period == 15: 
		pull_type = Client.KLINE_INTERVAL_15MINUTE 
	if period == '1d': 
		pull_type = Client.KLINE_INTERVAL_1DAY 
	if period == '1h': 
		pull_type = Client.KLINE_INTERVAL_1HOUR
	klines = client.get_historical_klines(ticker, pull_type, start, end)
	ohlc = pd.DataFrame({'open_time': [float(klines[i][0]) for i in range(len(klines))],
						 'open': [float(klines[i][1]) for i in range(len(klines))],
						 'high': [float(klines[i][2]) for i in range(len(klines))],
						 'low': [float(klines[i][3]) for i in range(len(klines))],
						 'close': [float(klines[i][4]) for i in range(len(klines))],
						 'volume': [float(klines[i][5]) for i in range(len(klines))],
						 'close_time': [float(klines[i][6]) for i in range(len(klines))],
						 'num_trades': [float(klines[i][7]) for i in range(len(klines))]})
	ohlc['price'] = (ohlc['high'] + ohlc['low'])/2
	return(ohlc)


#Returns Order Book IN REAL TIME
def pullBook(ticker): 
	time_stamp = datetime.datetime.utcfromtimestamp(time.time()).strftime('%Y-%m-%dT%H:%M:%SZ')
	depth = client.get_order_book(symbol=ticker)
	#Convert API output to a OHLC type order book
	bid_price = [float(depth['bids'][i][0]) for i in range(len(depth['bids']))]
	bid_volume = [float(depth['bids'][i][1]) for i in range(len(depth['bids']))]
	ask_price = [float(depth['asks'][i][0]) for i in range(len(depth['asks']))]
	ask_volume = [float(depth['asks'][i][1]) for i in range(len(depth['asks']))]
	#Convert to Data Frame: 
	order_book = pd.DataFrame({'time_stamp': [time_stamp], 
							   'id': depth['lastUpdateId'],
							   'open_bid': bid_price[0],
							   'high_bid': max(bid_price),
							   'low_bid': min(bid_price),
							   'close_bid': bid_price[len(bid_price)-1],
							   'average_bid': np.mean(bid_price),
							   'volume_bid': sum(bid_volume),
							   'open_ask': ask_price[0],
							   'high_ask': max(ask_price),
							   'low_ask': min(ask_price),
							   'close_ask': ask_price[len(ask_price)-1],
							   'average_ask': np.mean(ask_price), 
							   'volume_ask': sum(ask_volume)})
	return(order_book)


def generateBook(ticker, max_pulls = 6000): 
	order_book = pd.DataFrame()
	#60 pulls --> 1 minute worth of data 
	n_pulls = 0
	while n_pulls < max_pulls: 
		start = time.time()
		try:
			pull = generateBook('BTC')
		except Exception as e:
			print(e)
			break
		else: 
			order_book = order_book.append(pull)
			time_delta = time.time() - start 
			if time_delta < 0.8: 
				time.sleep(1-time_delta)
			n_pulls = n_pulls + 1	
			print("Pull No. " + str(n_pulls) + ", Time: " + \
			datetime.datetime.utcfromtimestamp(start).strftime('%Y-%m-%dT%H:%M:%SZ'))
	return(order_book)




