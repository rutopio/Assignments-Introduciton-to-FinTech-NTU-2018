import sys
import numpy as np
import pandas as pd
from myStrategy import myStrategy

dailyOhlcv = pd.read_csv(sys.argv[1])
minutelyOhlcv = pd.read_csv(sys.argv[2])
# 讀取csv
# print(dailyOhlcv)
# 這裡看得到全部的資料（到 2017/12/30）

evalDays = 1
action = np.zeros((evalDays,1))
openPricev = dailyOhlcv["open"].tail(evalDays).values
#print(openPricev)
# 最後一天（最新一天, 2017/12/30）的開盤值

# print(dailyOhlcv)
# print(openPricev)

#print("for start")    
for ic in range(evalDays,0,-1):
    dailyOhlcvFile = dailyOhlcv.head(len(dailyOhlcv)-ic)
    # 過去每一筆的OHLCV 到 2017/12/29 最後一天
    #print(dailyOhlcvFile)    
    # dateStr = dailyOhlcvFile.iloc[-1,0]
    # 原始的檔案
    dateStr = dailyOhlcvFile.iloc[-1,1]
    # 目標要讀出日期 這裡會讀出2017/12/29的日期 最後一天
    #print(dateStr)
    
    #minutelyOhlcvFile = minutelyOhlcv.head((np.where(minutelyOhlcv.iloc[:,0].str.split(expand=True)[0].values==dateStr))[0].max()+1)
    # 讀出當天（2017/12/29）的分鐘OHLCV
    #print(openPricev[evalDays-ic])
    # openPricev[evalDays-ic] 這裡是當天的價格
    minutelyOhlcvFile = 0
    #print("for end")    
    action[evalDays-ic] = myStrategy(dailyOhlcvFile,minutelyOhlcvFile,openPricev[evalDays-ic])
    # 所以傳到myStrategy裡的會有 dailyOhlcvFile 過去為止的OHCLV , minutelyOhlcvFile 昨天的OHLC ,openPricev[evalDays-ic] 當天的價格



print(action)

