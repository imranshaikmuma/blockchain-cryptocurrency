

#detecting hot coin


# for each in market_id:
	# buyorders = requests.get('https://www.coinexchange.io/api/v1/getorderbook?market_id=' + str(each))
	# buyorders_pandas = pd.read_json(buyorders.text)
	# buyorders_result = buyorders_pandas['result']['BuyOrders']
	# if len(buyorders_result) != 0:
		# buyorders_df = pd.DataFrame({'buyorders':buyorders_result})
		# buyorders_panel = pd.Panel({'buyorders': buyorders_df['buyorders'].apply(pd.Series)})
		# buyorders = buyorders_panel.buyorders
		# buyorders['market_id']=each
		# buyorders = buyorders.sort_values(by=['OrderTime'], ascending=False)
		# buyorders = buyorders.reset_index(drop=True)
		# nooforders = buyorders.shape[0]
		# orderdate = datetime.strptime(buyorders['OrderTime'][0].split(' ')[0],'%Y-%m-%d') - datetime.strptime(buyorders['OrderTime'][nooforders-1].split(' ')[0],'%Y-%m-%d')
		# ordertime = datetime.strptime(buyorders['OrderTime'][0].split(' ')[1],'%H:%M:%S') - datetime.strptime(buyorders['OrderTime'][nooforders-1].split(' ')[1],'%H:%M:%S')
		# tradedensity[each]=[orderdate.days,ordertime.seconds,nooforders,markets[markets.MarketID == each]['MarketAssetName'].iloc[0],markets[markets.MarketID == each]['BaseCurrency'].iloc[0] ]
		
# tradedensity = pd.DataFrame.from_dict(tradedensity,orient='index')
# tradedensity.columns = ['days','seconds','buyorders','assetname','baseprice']
# tradedensity = tradedensity.sort_values(by=['buyorders','days', 'seconds'],ascending=[False,True,True])
# tradedensity = tradedensity.reset_index(drop=True)
# print(tradedensity)


#price change every 5 min,price 24hr change, volume every 5 minutes, buy order  every 5 minutes, sell order every 5 minutes, tradecount 24hr, 24hr low, 24hr high


def coinmarketdata():
	
	count = 5
	import coinmarketcap
	import json
	import pandas as pd
	import time
	import pickle
	import os.path
	import timeit
	start_time = timeit.default_timer()

	market = coinmarketcap.Market()
	coin = market.ticker(limit=0)

	parsedCoin = json.loads(json.dumps(coin))
	parsedCoin = json.dumps(parsedCoin, indent=4, sort_keys=True)
	df = pd.read_json(parsedCoin)
	df_sort_change1h = df.sort_values(by=['percent_change_1h'], ascending=False)
	#print(df_sort_change1h)

	import requests
	import datetime
	from datetime import datetime
	markets = requests.get('https://www.coinexchange.io/api/v1/getmarkets')
	markets_pandas = pd.read_json(markets.text)
	markets_result = markets_pandas['result']
	markets_df = pd.Series.to_frame(markets_result)
	markets_panel = pd.Panel({'markets': markets_df['result'].apply(pd.Series)})
	markets = markets_panel.markets
	#print(markets)

	market_id = markets['MarketID']
	
	if os.path.isfile('coinoutput.pkl') == True:
		with open('coinoutput.pkl','rb') as f:
			lastprice,pricechange24hr,pricechange,volume,buyorderscount,sellorderscount,tradecount24hr,highprice,lowprice,buyorder24hr,sellorder24hr = pickle.load(f)
	else:
		lastprice = [None]*12	
		pricechange=[None]*12
		volume = [None]*12
		buyorderscount = [None]*12
		sellorderscount =  [None]*12
		
	coinanalysis = dict()
	buytradedensity = dict()
	selltradedensity = dict()

	for index, row in markets.iterrows():
		if row['Active'] == True and row['BaseCurrencyCode'] == 'BTC':
			marketid= row['MarketID']
			
			lastprice2 = lastprice
			
			assetname = row['MarketAssetName']
			coinanalysis[assetname]= []
			
			lastprice = [lastprice[-1]] + lastprice[:-1]
			volume = [volume[-1]] + volume[:-1]
			buyorderscount = [buyorderscount[-1]] + buyorderscount[:-1]
			sellorderscount = [buyorderscount[-1]] + buyorderscount[:-1]
			
			marketsummary = requests.get('https://www.coinexchange.io/api/v1/getmarketsummary?market_id='+str(marketid))
			marketsummary_pandas = pd.read_json(marketsummary.text)
			marketsummary_result = marketsummary_pandas['result']
			
			lastprice[0]=marketsummary_result["LastPrice"]
			volume[0] = marketsummary_result["Volume"]
			
			for i in range(0,len(lastprice)):
				if (lastprice2[i] != None) & (lastprice[i] != None):
					pricechange[i]= ((lastprice[i] -lastprice2[i])/lastprice2[i])* 100
				else:
					pricechange[i]= None
					
			tradecount24hr = marketsummary_result["TradeCount"]
			highprice = marketsummary_result["HighPrice"]
			lowprice = marketsummary_result["LowPrice"]
			pricechange24hr = marketsummary_result["Change"]
			buyorder24hr = marketsummary_result["BuyOrderCount"]
			sellorder24hr = marketsummary_result["BuyOrderCount"]
			
			
			orders = requests.get('https://www.coinexchange.io/api/v1/getorderbook?market_id=' + str(marketid))
			orders_pandas = pd.read_json(orders.text)
			buyorders_result = orders_pandas['result']['BuyOrders']
			if len(buyorders_result) != 0:
				buyorders_df = pd.DataFrame({'buyorders':buyorders_result})
				buyorders_panel = pd.Panel({'buyorders': buyorders_df['buyorders'].apply(pd.Series)})
				buyorders = buyorders_panel.buyorders
				buyorders['market_id']=marketid
				buyorders = buyorders.sort_values(by=['OrderTime'], ascending=False)
				buyorders = buyorders.reset_index(drop=True)
				
				utcnow = datetime.utcnow()
				utchour = utcnow.hour
				utcminute = utcnow.minute
				utcsecond = utcnow.second
				utctime = str(utchour) + ':' + str(utcminute) + ':' + str(utcsecond)
				
				utcday = utcnow.day
				utcmonth = utcnow.month
				utcyear = utcnow.year
				utcdate = str(utcyear) + '-' + str(utcmonth) + '-' + str(utcday)
				
				
				
				buyordercount = 0
				for index,row in buyorders.iterrows():
					dayelapse = datetime.strptime(utcdate,'%Y-%m-%d') - datetime.strptime(row['OrderTime'].split(' ')[0],'%Y-%m-%d')
					timeelapse = datetime.strptime(utctime,'%H:%M:%S') - datetime.strptime(row['OrderTime'].split(' ')[1],'%H:%M:%S')
					if timeelapse.seconds <= 300 & dayelapse.days==0 :
						buyordercount =+ 1
				
			
				nooforders = buyorders.shape[0]
				orderdate = datetime.strptime(buyorders['OrderTime'][0].split(' ')[0],'%Y-%m-%d') - datetime.strptime(buyorders['OrderTime'][nooforders-1].split(' ')[0],'%Y-%m-%d')
				ordertime = datetime.strptime(buyorders['OrderTime'][0].split(' ')[1],'%H:%M:%S') - datetime.strptime(buyorders['OrderTime'][nooforders-1].split(' ')[1],'%H:%M:%S')
				buytradedensity[marketid]=[orderdate.days,ordertime.seconds,nooforders,markets[markets.MarketID == marketid]['MarketAssetName'].iloc[0],markets[markets.MarketID == marketid]['BaseCurrency'].iloc[0] ]
			
			buyorderscount [0] = buyordercount
			
			sellorders_result = orders_pandas['result']['SellOrders']
			if len(sellorders_result) != 0:
				sellorders_df = pd.DataFrame({'sellorders':sellorders_result})
				sellorders_panel = pd.Panel({'sellorders': sellorders_df['sellorders'].apply(pd.Series)})
				sellorders = sellorders_panel.sellorders
				sellorders['market_id']=marketid
				sellorders = sellorders.sort_values(by=['OrderTime'], ascending=False)
				sellorders = sellorders.reset_index(drop=True)
				
				utcnow = datetime.utcnow()
				utchour = utcnow.hour
				utcminute = utcnow.minute
				utcsecond = utcnow.second
				utctime = str(utchour) + ':' + str(utcminute) + ':' + str(utcsecond)
				
				utcday = utcnow.day
				utcmonth = utcnow.month
				utcyear = utcnow.year
				utcdate = str(utcyear) + '-' + str(utcmonth) + '-' + str(utcday)
				
				
				sellordercount = 0
				for index,row in sellorders.iterrows():
					dayelapse = datetime.strptime(utcdate,'%Y-%m-%d') - datetime.strptime(row['OrderTime'].split(' ')[0],'%Y-%m-%d')
					timeelapse = datetime.strptime(utctime,'%H:%M:%S') - datetime.strptime(row['OrderTime'].split(' ')[1],'%H:%M:%S')
					if timeelapse.seconds <= 300 & dayelapse.days==0 :
						sellordercount =+ 1
				
			
				nooforders = sellorders.shape[0]
				orderdate = datetime.strptime(sellorders['OrderTime'][0].split(' ')[0],'%Y-%m-%d') - datetime.strptime(sellorders['OrderTime'][nooforders-1].split(' ')[0],'%Y-%m-%d')
				ordertime = datetime.strptime(sellorders['OrderTime'][0].split(' ')[1],'%H:%M:%S') - datetime.strptime(sellorders['OrderTime'][nooforders-1].split(' ')[1],'%H:%M:%S')
				selltradedensity[marketid]=[orderdate.days,ordertime.seconds,nooforders,markets[markets.MarketID == marketid]['MarketAssetName'].iloc[0],markets[markets.MarketID == marketid]['BaseCurrency'].iloc[0] ]
			
			sellorderscount [0] = sellordercount

			coinanalysis[assetname].extend(lastprice)
			coinanalysis[assetname].append(pricechange24hr)
			coinanalysis[assetname].extend(pricechange)
			coinanalysis[assetname].extend(volume)
			coinanalysis[assetname].extend(buyorderscount)
			coinanalysis[assetname].extend(sellorderscount)
			coinanalysis[assetname].append(tradecount24hr)
			coinanalysis[assetname].append(highprice)
			coinanalysis[assetname].append(lowprice)
			coinanalysis[assetname].append(buyorder24hr)
			coinanalysis[assetname].append(sellorder24hr)
				
						
	buytradedensity = pd.DataFrame.from_dict(buytradedensity,orient='index')
	buytradedensity.columns = ['days','seconds','buyorders','assetname','baseprice']
	buytradedensity = buytradedensity.sort_values(by=['buyorders','days', 'seconds'],ascending=[False,True,True])
	buytradedensity = buytradedensity.reset_index(drop=True)
	
	
	selltradedensity = pd.DataFrame.from_dict(selltradedensity,orient='index')
	selltradedensity.columns = ['days','seconds','buyorders','assetname','baseprice']
	selltradedensity = selltradedensity.sort_values(by=['buyorders','days', 'seconds'],ascending=[False,True,True])
	selltradedensity = selltradedensity.reset_index(drop=True)
	#print(tradedensity)

	with open('coinoutput.pkl','wb') as f:
		pickle.dump((lastprice,pricechange24hr,pricechange,volume,buyorderscount,sellorderscount,tradecount24hr,highprice,lowprice,buyorder24hr,sellorder24hr),f,-1)
		
	coinanalysis = pd.DataFrame.from_dict(coinanalysis,orient='index')
	coinanalysis.columns = ['LP5','LP10','LP15','LP20','LP25','LP30','LP35','LP40','LP45','LP50','LP55','LP60', '24hr Price Change', 
							'PC5','PC10','PC15','PC20','PC25','PC30','PC35','PC40','PC45','PC50','PC55','PC60',
							'V5','V10','V15','V20','V25','V30','V35','V40','V45','V50','V55','V60',
							'BO5','BO10','BO15','BO20','BO25','BO30','BO35','BO40','BO45','BO50','BO55','BO60',
							'SO5','SO10','SO15','SO20','SO25','SO30','SO35','SO40','SO45','SO50','SO55','SO60',
							'24hr Trade count', 'High Price 24hr', 'Low Price 24hr', 'Buy Order 24hr', 'Sell Order 24hr']

	
	
	#print(coinanalysis)
	
	if count%60 == 0:
		writer = pd.ExcelWriter('output'+str(utcnow).replace(':','')+'.xlsx')
		print('saved')
		coinanalysis.to_excel(writer,'Sheet1')
		writer.save()
	else:
		count += 5
	
	elapsed = timeit.default_timer() - start_time
	print('timeofexecution',elapsed)
	
	time.sleep(10)
	
while True:
    coinmarketdata()
	
	
							
							

	