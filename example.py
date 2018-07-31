tickers = returnTickers()
#To just get tickers trading on USDT basis: 
tickers = returnTickers("USDT")
#Generate Predictions
from joblib import Parallel, delayed
import multiprocessing

num_cores = multiprocessing.cpu_count()
predictions = Parallel(n_jobs = 6)(delayed(generatePrediction)(ticker, n_ahead=10) for ticker in tickers)
#Example of running a basic technical indicator model: 
df = pd.DataFrame({'Ticker': [predictions[i][0] for i in range(len(predictions))],
							  'CurrentPrice': [predictions[i][1]*100 for i in range(len(predictions))],
							  'EstimatedPrice': [predictions[i][2]*100 for i in range(len(predictions))],
							  'ExpectedReturn': [predictions[i][3]*100 for i in range(len(predictions))],
							  'Volume': [predictions[i][4] for i in range(len(predictions))]}, 
							  columns = ["Ticker", "CurrentPrice", "EstimatedPrice", "ExpectedReturn", "Volume"])
#Sort by expected returns:
sorted_df = df.sort_values(['ExpectedReturn', 'Volume'], ascending=False)
sorted_df = sorted_df.drop(sorted_df[sorted_df.Volume <= 0].index)
print sorted_df[:15]

#Grab data: 
#Change to fit needs: 
path_name = '/Users/...' 
for ticker in tickers: 
	df = generateHistoricalData(ticker, '1 Jan, 2017', '31 Mar, 2018', period = '1h')
	file_name = path_name+ticker + '.csv'
	df.to_csv(file_name)
	print(ticker)