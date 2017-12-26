import requests
import pandas as pd

markets = requests.get('https://www.coinexchange.io/api/v1/getmarkets')
markets_pandas = pd.read_json(markets.text)
markets_result = markets_pandas['result']
markets_df = pd.Series.to_frame(markets_result)
markets_panel = pd.Panel({'markets': markets_df['result'].apply(pd.Series)})
markets = markets_panel.markets
#print(markets)

market_id = markets['MarketID']

marketsummary = requests.get('https://www.coinexchange.io/api/v1/getmarketsummaries')
marketsummary_pandas = pd.read_json(marketsummary.text)
marketsummary_result = marketsummary_pandas['result']
marketsummary_df = pd.Series.to_frame(marketsummary_result)
marketsummary_panel = pd.Panel({'marketsummary': marketsummary_df['result'].apply(pd.Series)})
marketsummary = marketsummary_panel.marketsummary
#print(marketsummary)

count = 0
for each in market_id:
	if count==0:
		sellorders = requests.get('https://www.coinexchange.io/api/v1/getorderbook?market_id=' + str(each))
		sellorders_pandas = pd.read_json(sellorders.text)
		sellorders_result = sellorders_pandas['result']['SellOrders']
		if len(sellorders_result) != 0:
			sellorders_df = pd.DataFrame({'sellorders':sellorders_result})
			sellorders_panel = pd.Panel({'sellorders': sellorders_df['sellorders'].apply(pd.Series)})
			sellorders = sellorders_panel.sellorders
			sellorders['market_id']=each
			count+=1
	else:
		sellorders2 = requests.get('https://www.coinexchange.io/api/v1/getorderbook?market_id=' + str(each))
		sellorders2_pandas = pd.read_json(sellorders2.text)
		sellorders2_result = sellorders2_pandas['result']['SellOrders']
		if len(sellorders2_result) != 0:
			sellorders2_df = pd.DataFrame({'sellorders':sellorders2_result})
			sellorders2_panel = pd.Panel({'sellorders': sellorders2_df['sellorders'].apply(pd.Series)})
			sellorders2 = sellorders2_panel.sellorders
			sellorders2['market_id']=each
			sellorders = sellorders.append(sellorders2,ignore_index=True)
			count+=1

count = 0
for each in market_id:
	if count==0:
		buyorders = requests.get('https://www.coinexchange.io/api/v1/getorderbook?market_id=' + str(each))
		buyorders_pandas = pd.read_json(buyorders.text)
		buyorders_result = buyorders_pandas['result']['BuyOrders']
		if len(buyorders_result) != 0:
			buyorders_df = pd.DataFrame({'buyorders':buyorders_result})
			buyorders_panel = pd.Panel({'buyorders': buyorders_df['buyorders'].apply(pd.Series)})
			buyorders = buyorders_panel.buyorders
			buyorders['market_id']=each
			count+=1
	else:
		buyorders2 = requests.get('https://www.coinexchange.io/api/v1/getorderbook?market_id=' + str(each))
		buyorders2_pandas = pd.read_json(buyorders2.text)
		buyorders2_result = buyorders2_pandas['result']['BuyOrders']
		if len(buyorders2_result) != 0:
			buyorders2_df = pd.DataFrame({'buyorders':buyorders2_result})
			buyorders2_panel = pd.Panel({'buyorders': buyorders2_df['buyorders'].apply(pd.Series)})
			buyorders2 = buyorders2_panel.buyorders
			buyorders2['market_id']=each
			buyorders = buyorders.append(buyorders2,ignore_index=True)
			count+=1

print(buyorders)




