#Note(s): Technical Indicators
#Indicator functions modified from talib's original functions to: 
#1. Accomodate for pandas pd input 
#2. For all buy/sell indicators, return buy/sell signal arrays
import talib

#Simple Moving Average
def SMA(df, n = 30, midpoint = False):
	if midpoint == False: 
		return(talib.SMA(np.array(df.close), timeperiod = n))
	else:
		return(talib.SMA(np.array(df.price), timeperiod = n))


#Exponential Moving Average
def EMA(df, n = 30, midpoint = False):
	if midpoint == False: 
		return(talib.EMA(np.array(df.close), timeperiod = n))
	else:
		return(talib.EMA(np.array(df.price), timeperiod = n))

#Momentum
def Momentum(df, n = 10):
	return(talib.MOM(np.array(df.price), timeperiod = n))

#Volatility - True Range
def TrueRange(df): 
	return(talib.TRANGE(np.array(df.high), np.array(df.low), np.array(df.close)))

#---------------------------------------------------------------------------------------------------------
#Trend Strength Indicators: 
#---------------------------------------------------------------------------------------------------------
#Average Directional Movement Index (ADX)
#Higher number = stronger trend 
#Lower number = weaker trend
def ADX(df, n=30):
	return(talib.ADX(np.array(df.high), np.array(df.low), np.array(df.close), timeperiod = n))

#Aroon Oscillator
#Indication for how strong / weak the trend is 
def Aroon(df, n=15): 
	return(talib.AROONOSC(np.array(df.high), np.array(df.low), timeperiod = n))

#Directional Movement Index
#High number --> Strong Trend, low number --> Weak trend
def DMI(df, n=20): 
	return(talib.DX(np.array(df.high), np.array(df.low), np.array(df.close), timeperiod = n))

#---------------------------------------------------------------------------------------------------------
#Buy/Sell Indicators:
#---------------------------------------------------------------------------------------------------------
#MACD
def MACD(df, n_fast = 12, n_slow = 26, n_signal = 9): 
	macd, macdsignal, macdhist = talib.MACD(np.array(df.price), n_fast, n_slow, n_signal)
	indicator = macd - macdsignal
	buy_signal = np.where(np.isnan(indicator), indicator, np.where(((indicator > 0) & (macd > 0)), 1, 0))
	sell_signal = np.where(np.isnan(indicator), indicator, np.where(((indicator < 0) & (macd < 0)), 1, 0))
	return(buy_signal, sell_signal)

#CCI: 
#Normal range: -100 to 100, anything outside indicates oversold or overbought 
def CCI(df, n=15): 
	cci = talib.CCI(np.array(df.high), np.array(df.low), np.array(df.close), timeperiod = n)
	buy_signal = np.where(np.isnan(cci), cci, np.where(cci < -100, 1, 0))
	sell_signal = np.where(np.isnan(cci), cci, np.where(cci > 100, 1, 0))
	return(buy_signal, sell_signal)


#Chande Momentum Oscillator
#If over 50 --> Overbought, Under -50 --> Undersold
#Can also use MA Of CMO; if crosses above --> buy signal, if crosses below --> sell signal
def CMO(df, n=20): 
	cmo = talib.CMO(np.array(df.price), timeperiod = n)
	buy_signal = np.where(np.isnan(cmo), cmo, np.where(cmo < -50, 1, 0))
	sell_signal = np.where(np.isnan(cmo), cmo, np.where(cmo > 50, 1, 0))
	return(buy_signal, sell_signal)

#RSI
#Overbought/oversold indicator when the value is over 70/below 30
def RSI(df, n=15):
	rsi = talib.RSI(np.array(df.price), timeperiod = n)
	buy_signal = np.where(np.isnan(rsi), rsi, np.where(rsi < 30, 1, 0))
	sell_signal = np.where(np.isnan(rsi), rsi, np.where(rsi > 70, 1, 0))
	return(buy_signal, sell_signal)

#Stochastic Oscillator
#%D values over 75 indicate an overbought condition; values under 25 indicate an oversold condition
#When the Fast %D crosses above the Slow %D, it is a buy signal; when it crosses below, it is a sell signal
def stochasticOscillator(df): 
	slowk, slowd = talib.STOCH(np.array(df.high), np.array(df.low), np.array(df.close))
	fastk, fastd = talib.STOCHF(np.array(df.high), np.array(df.low), np.array(df.close))
	buy_signal = np.where(np.isnan(slowd), slowd, np.where(slowd < 25, 1, 0))
	buy_signal = buy_signal * np.where(np.isnan(slowd), slowd, np.where(fastd > slowd, 1, 0))
	sell_signal = np.where(np.isnan(slowd), slowd, np.where(slowd > 75, 1, 0))
	sell_signal = sell_signal * np.where(np.isnan(slowd), slowd, np.where(fastd < slowd, 1, 0))
	return(buy_signal, sell_signal)

#Volume: 
#Chaikin A/D Oscillator
#When the Chaikin Oscillator crosses above zero, it indicates a buy signal
#When it crosses below zero it indicates a sell signal
def Chaikin(df): 
	chaikin = talib.ADOSC(np.array(df.high), np.array(df.low), np.array(df.close), np.array(df.volume))
	buy_signal = np.where(np.isnan(chaikin), chaikin, np.where(chaikin > 0, 1, 0))
	sell_signal = np.where(np.isnan(chaikin), chaikin, np.where(chaikin < 0, 1, 0))
	return(buy_signal, sell_signal)


