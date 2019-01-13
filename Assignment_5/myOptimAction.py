'''
B05102074 何青儒 2018-11-19

- What is your strategy for determining the timings for "buy" and "sell"?

假設一開始會有兩種狀況：持有 1 塊錢的現金（cash，單位是元）跟用當下價格（priceVec[0]）、以 1 塊錢買的股數（stock，單位是股數）
所以初始值 cash = 1
　　　　　 stock = 1/priceVec[0]

此時第i天會有兩種狀況：當天結束的當下持有現金或是持有股票：

cash		=  max(cash , 						stock*(priceVec[i]*(1-transFeeRate)))
當天持有現金	   昨天持有現金						賣掉昨天所持有的股票，扣除交易手續費後實際所得
				（即什麼都不做，actionVec[i] = 0） （actionVec[i] = -1）

如果「昨天持有現金」所得到的現值會比「賣掉昨天所持有的股票」還要多，那麼今天會什麼都不做，反之我們會賣出昨天的股票


stock	 	= max(stock , 						cash/(priceVec[i]*(1+transFeeRate)))
當天持有股數	   昨天持有股票						用昨天的錢買進股票，扣除交易手續費後實際股數
				（即什麼都不做，actionVec[i] = 0） （actionVec[i] = 1）

如果「昨天持有股數」所得到的現值會比「用昨天的錢買入的股票」現值還要多，那麼今天會什麼都不做，反之我們會買入股票

我們要做的就是每天針對這兩種狀況都做最大化，並在最後回溯回去求最佳路線。



- How does it work on SPY dataset?

但其實我的回溯是有問題的QQ，寫到後來我自己是還找不到出了哪裡的問題，可能需要冷靜個幾天回來看才抓的到。
（可以說是動態規劃沒學好ㄞ）

舉SPY.csv這個檔案來說，不管actionVec要寫入1, -1, 0的話，
直接做計算最終求得的回報率應該是217.5240580935958倍，
但做完回溯後實際回報率（用profitEstimateOpen01.py去跑）會得到209.01084382倍。

雖然我還沒找到問題，但我覺得是出在最一開始幾筆資料（回溯回去會是最後幾筆）

舉judge系統而例，多數人（正解）是478422351，但我只有440943004。
'''


def myOptimAction(priceVec, transFeeRate):
	import numpy as np

	# 先檢查共有幾筆資料
	dataLen = len(priceVec)
	
	# 預設的 actionVec 都是零（就是什麼都不做），大小等長於datalen
	actionVec = np.zeros(dataLen)
	
	# set as default
	cash = 1
	stock = 0
	
	# for backtracking
	cash_index = np.zeros(dataLen)
	stock_index = np.zeros(dataLen)
	

	for i in range(0,dataLen):

		# 這幾個 if 是為了回溯而寫入的index
		if cash > stock*(priceVec[i]*(1-transFeeRate)):
			cash_index[i] = 0 # stock
		elif cash < stock*(priceVec[i]*(1-transFeeRate)):
			cash_index[i] = -1 # sell

		if stock > cash/(priceVec[i]*(1+transFeeRate)):
			stock_index[i] = 0 # keep
		elif stock < cash/(priceVec[i]*(1+transFeeRate)):
			stock_index[i] = 1 # buy
		
		# maximized two situation，最主要進行計算的地方
		cash = max(cash , stock*(priceVec[i]*(1-transFeeRate)))
		stock = max(stock , cash/(priceVec[i]*(1+transFeeRate)))		

	# 如果不做回溯的話，最終跑出來的值是
	# 217.5240580935958 for SPY.csv
	stockvalue = stock*priceVec[-1]*(1-transFeeRate)
	maxvalue = max(cash,stockvalue)
	#print(maxvalue)

	# 以下開始回溯
	# 1 for cash track ,and -1 for stock track
	flag = 0
	
	# 考慮最後一筆是持有現金cash比較好，還是持有股票的現值stock*priceVec[-1]*(1-transFeeRate)比較好
	if cash > stock*priceVec[-1]*(1-transFeeRate):
		actionVec[-1] = cash_index[-1]
		flag = 1 # cash track
	elif cash < stock*priceVec[-1]*(1-transFeeRate):
		actionVec[-1] = stock_index[-1]
		flag = -1 # stock track

	for i in range(dataLen-1,-1,-1):
		if  flag == 1: # when on cash track
			actionVec[i] = cash_index[i]
			if actionVec[i] == -1:
				flag = -1 # change to stock track

		elif flag == -1: #stock line
			actionVec[i] = stock_index[i]
			if actionVec[i] == 1:
				flag = 1 # change to cash track
			
	return actionVec
