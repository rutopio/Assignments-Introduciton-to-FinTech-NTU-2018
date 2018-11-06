'''
x = list(range(10))

print(type(x),x)

'''
import sys
import numpy as np
import pandas as pd
import talib
#from myStrategy import myStrategy

df = pd.read_csv(sys.argv[1])
adjClose = df["Adj Close"].values
capital=1
capitalOrig=capital
dataCount=len(adjClose)

suggestedAction= np.zeros((dataCount,1))
stockHolding=np.zeros((dataCount,1))
total = np.zeros((dataCount,1))
realAction=np.zeros((dataCount,1))
total[0] = capital

#30,5,5,3,1,65,60,50,45

def myStrategy(pastData, currPrice, ma_long_day, ma_short_day, rsi_day, ma_long_type, ma_short_type, rsi_high_bull, rsi_low_bull, rsi_high_bear, rsi_low_bear):
    #def myStrategy(pastData, currPrice):
    #pastData是一群數字 currPrice是當今價格
    # 共有ma_long_day/ma_short_day/rsi_day/ma_long的matype/ma_short的matype/
    # 牛市時的rsi_high/牛市時的rsi_low/熊市時的rsi_high/熊市時的rsi_low
    # 9個
    #defalut
    action = 0
    bull_bear_index = 0
    # bull = -1
    # bear = 1
    # normal = 0

    #ma_long_type = 3
    #ma_short_type = 1

    comb = np.append(pastData,currPrice)
    
    #set
    #ma_long_day  = 30
    #ma_short_day = 5
    #rsi_day = 5
    # 發明人 Wilder 本人喜好用 14 天週期，而市場上有用 6 日、9 日或 12 日等不一。
    #calculate

    ma_long = (talib.MA(comb, timeperiod = ma_long_day, matype = ma_long_type))[-1]
    ma_short = (talib.MA(comb, timeperiod = ma_short_day, matype = ma_short_type))[-1]
    rsi_current = (talib.RSI(comb, timeperiod = rsi_day))[-1]

    # matype 0=sma 1=ema 2=wma 3=dema 4=tema

    if(ma_long>ma_short):
        bull_bear_index = 1
        #bear
        #長線趨勢高於近期趨勢，代表近期熊
    elif(ma_long<ma_short):
        bull_bear_index = (-1)
        #bull
        #長線趨勢低於近期趨勢，代表近期牛
    else:
        bull_bear_index = 0


    if(bull_bear_index == (-1)):
        #bull
        #rsi_high_bull = 65
        #rsi_low_bull = 60
        if (rsi_current>=rsi_high_bull):
        #sell
            action = -1
        elif (rsi_current<=rsi_low_bull):
        #buy
            action=1
        else:
        #do nothing
            action=0
    
    elif(bull_bear_index == 1):
        #bear
        #rsi_high_bear = 50
        #rsi_low_bear = 45
        if (rsi_current>=rsi_high_bear):
        #sell
            action= -1
        elif (rsi_current<=rsi_low_bear):
        #buy
            action=1
        else:
        #do nothing
            action=0
    
    return action
ct = 0
#30,5,5,3,1,65,60,50,45
#pastData, currPrice, ma_long_day, ma_short_day, rsi_day, ma_long_type, ma_short_type, rsi_high_bull, rsi_low_bull, rsi_high_bear, rsi_low_bear
#                       14-60       5-10            5-14    0-4         -   0-4         50-70           40-60       50-70          40-60
maxreturn = 0
for ma_long_day in range(50,61):
    for ma_short_day in range(4,15):
        for rsi_day in range(4,15): 
            for ma_long_type in range(3,5):
                for ma_short_type in range(3,5):
                    for rsi_high_bull in range(50,70):
                        for rsi_low_bull in range(40,rsi_high_bull):
                            for rsi_high_bear in range(40,60):
                                for rsi_low_bear in range(30,rsi_high_bear):
                                    capital=1
                                    capitalOrig=capital
                                    suggestedAction= np.zeros((dataCount,1))
                                    stockHolding=np.zeros((dataCount,1))
                                    total = np.zeros((dataCount,1))
                                    realAction=np.zeros((dataCount,1))
                                    total[0] = capital
                                
                                    for ic in range(dataCount):
                                        currPrice=adjClose[ic]    
                                        suggestedAction[ic]=myStrategy(adjClose[0:ic], currPrice,ma_long_day,ma_short_day, rsi_day, ma_long_type, ma_short_type, rsi_high_bull, rsi_low_bull, rsi_high_bear, rsi_low_bear)
                                        if ic > 0:
                                            stockHolding[ic]=stockHolding[ic-1]
                                        if suggestedAction[ic] == 1:
                                            if stockHolding[ic]==0:            
                                                stockHolding[ic]=capital/currPrice
                                                capital=0
                                                realAction[ic]=1
                                        elif suggestedAction[ic] == -1:
                                            if stockHolding[ic]>0:
                                                capital=stockHolding[ic]*currPrice
                                                stockHolding[ic]=0
                                                realAction[ic]=-1
                                        elif suggestedAction[ic] == 0:
                                            realAction[ic]=0
                                        else:
                                            assert False
                                        total[ic]=capital+stockHolding[ic]*currPrice
                                        
                                    returnRate=(total[-1]-capitalOrig)/capitalOrig   
                                    ct = ct+1  
                                    if(returnRate > maxreturn):
                                        
                                        maxreturn = returnRate
                                        max_ma_long_type = ma_long_type
                                        max_ma_short_type = ma_short_type
                                        max_ma_long_day = ma_long_day
                                        max_ma_short_day = ma_short_day
                                        max_rsi_day = rsi_day
                                        max_rsi_high_bull = rsi_high_bull
                                        max_rsi_low_bull = rsi_low_bull
                                        max_rsi_high_bear = rsi_high_bear
                                        max_rsi_low_bear = rsi_low_bear
                                        max_ct = ct
                                    print('Index:',ct,'|當今報酬:', returnRate, '最大報酬:', maxreturn,'發生在:',max_ct,'(', max_ma_long_day,max_ma_short_day,max_rsi_day,max_ma_long_type,max_ma_short_type,max_rsi_high_bull,max_rsi_low_bull,max_rsi_high_bear,max_rsi_low_bear,')','|MA長:',ma_long_day,'|MA短:', ma_short_day,'|RSI天:', rsi_day,'|MA長type:', ma_long_type,'|MA短type:', ma_short_type, '|牛高:',rsi_high_bull,'|牛低:', rsi_low_bull, '|熊高:',rsi_high_bear,'|熊低:', rsi_low_bear)


print('======================DONE=========================')
print('TOTAL COUNT : ',ct)
print('HAPPEN COUNT : ',max_ct)
print('MAX RETURN :',maxreturn)
print('MA LONG DAY : ',max_ma_long_day)
print('MA SHORT DAY : ',max_ma_short_day)
print('RSI DAY : ',max_rsi_day)
print('MA LONG TYPE : ',max_ma_long_type)
print('MA SHORT TYPE : ',max_ma_short_type)
print('RSI HIGH BEAR : ',max_rsi_high_bear)
print('RSI LOW BEAR : ',max_rsi_low_bear)
print('RSI HIGH BULL : ',max_rsi_high_bull)
print('RSI LOW BULL : ',max_rsi_low_bull)
print('======================DONE=========================')

