import coinmarketcap
import json
import pandas as pd
import time
import pickle

market = coinmarketcap.Market()
coin = market.ticker(limit=0)

parsedCoin = json.loads(json.dumps(coin))
parsedCoin = json.dumps(parsedCoin, indent=4, sort_keys=True)
print(type(parsedCoin))

df = pd.read_json(parsedCoin)

print(df)

id = df['id']
print(id)


import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import Select

path_to_chromedriver = r'C:\Users\intern4\Downloads\chromedriver_win32\chromedriver.exe'
browser = webdriver.Chrome(executable_path = path_to_chromedriver)

pastdata = dict()

url = 'https://coinmarketcap.com/currencies/'
for each in id:

	cryptoid = each.lower()
	url = url + str(cryptoid) + '/historical-data/'
	print(url)
	worksheet = workbook.add_worksheet(each)
	pastdata[each]=list()
	try:
		browser.get(url)
		main_window_handle = browser.current_window_handle
		browser.find_element_by_id('reportrange').click()
		browser.find_element_by_xpath('/html/body/div[8]/div[3]/ul/li[6]').click()
		table = browser.find_element_by_xpath('//*[@id="historical-data"]/div/div[3]/table/tbody')
		
		for tr in table.find_elements_by_tag_name('tr'):
			cryptodata = list()
			for j in tr.text.split(' '):
				cryptodata.append(j)
			pastdata[each].append(cryptodata)
		
		time.sleep(0.2)
		url = 'https://coinmarketcap.com/currencies/'
	except: 
		url = 'https://coinmarketcap.com/currencies/'
		continue
		
with open('historydata.pkl','wb') as f:
	pickle.dump(pastdata,f,-1)





