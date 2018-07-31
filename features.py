from import_data import *
from indicators import *
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from termcolor import colored, cprint 

#Period = period for which we are computing returns 
def getReturns(df, period = 10): 
	returns = df['price'].pct_change(period)
	returns = returns.dropna(axis=0, how = 'all')
	na_pad = pd.DataFrame(np.repeat(np.NaN, period))
	returns = returns.append(na_pad)
	returns.columns = ['Return']
	return(returns.reset_index(drop=True))

#Period refers to the number of minutes ahead for which we are forecasting to
def getFuturePrice(df, period = 5): 
	price = df['price'][:-period]
	na_pad = pd.DataFrame(np.repeat(np.NaN, period))
	price = price.append(na_pad)
	price.columns = ['futurePrice']
	return(price.reset_index(drop=True))

def computeIndicators(df): 
	#Initialize empty data frame
	features = pd.DataFrame()
	#Indicator Buy & Sell signals (1's and 0's)
	signals = [MACD, CCI, CMO, RSI, stochasticOscillator, Chaikin]
	for func in signals:
		buy, sell = func(df)
		features[func.__name__ + "_buy"] = buy
		features[func.__name__+ "_sell"] = sell
	#Trendlines 
	trends = [EMA, Momentum, TrueRange]
	for func in trends: 
		features[func.__name__] = func(df)
	#Different Moving Averages: 
	features['SMA7'] = SMA(df, 7)
	features['SMA25'] = SMA(df, 25)
	#Trend Strength (Constructed as an interaction term with SMA)
	trend_strength = [ADX, Aroon, DMI]
	for func in trend_strength: 
		cross_term = func(df)*features.SMA7
		features[func.__name__]=cross_term
	return(features)

print_negative = lambda x: cprint(x, "red", attrs = ['bold'])
print_positive = lambda x: cprint(x, "green", attrs = ['bold'])

#n_ahead = number of periods over which we wish to forecast returns (default at 10 min)
def generatePrediction(ticker, n_ahead = 5): 
	df = generateOHLC(ticker)
	data = pd.concat([getFuturePrice(df, period = n_ahead), computeIndicators(df)], axis=1)
	new_data = data.tail(1)
	new_data = new_data.drop('futurePrice', axis=1) #new_data.drop('Return')
	data = data.dropna(axis=0, how = 'any')
	target = data['futurePrice'] #target = data['Return']
	features = data.drop('futurePrice', axis=1)
	#Fit model: 
	lm = LinearRegression()
	lm.fit(features, target)
	estPrice = lm.predict(new_data)[0]
	currentPrice = df.tail(1)['price'].values[0]
	expectedReturn = (estPrice - currentPrice)/currentPrice
	currentVolume = df.tail(1)['volume'].values[0]
	#Print information: 
	if expectedReturn > 0: 
		print_positive(ticker)
		print_positive("Expected Return: " + str(expectedReturn*100) + "%")
	else: 
		print_negative(ticker)
		print_negative("Expected Return: " + str(expectedReturn*100) + "%")
	#print "Ticker: " + ticker
	#print "Expected Price: " + str(estPrice)
	#print "Expected Return: " + str(expectedReturn*100) + "%"
	#print "Current Volume Traded: "  + str(currentVolume)
	return([ticker, currentPrice, estPrice, expectedReturn, currentVolume])

#Need to add in cross validation component
def computeBacktest(ticker, n_ahead = 5): 
	df = generateOHLC(ticker)
	data = pd.concat([getFuturePrice(df, period = n_ahead), computeIndicators(df)], axis=1)
	data = data.dropna(axis=0, how = 'any')
	#Set up target & feature vectors
	target = data['futurePrice'] #target = data['Return']
	features = data.drop('futurePrice', axis=1)
	#Set up training/testing sets: 
	n = len(features)
	cutoff = int(round(2*n/3))
	xtrain = features[:cutoff]
	xtest = features[cutoff:]
	ytrain = target[:cutoff]
	ytest = target[cutoff:]
	#Fit Model
	lm = LinearRegression()
	lm.fit(xtrain, ytrain)
	ypred = lm.predict(xtest)
	#Plot results and print error
	print("Mean Absolute Error: " + str(np.mean(abs(ypred - ytest))))
	time = range(len(ytest))
	plt.plot(time, ytest, 'black')
	plt.plot(time, ypred, 'red')
	plt.show()






