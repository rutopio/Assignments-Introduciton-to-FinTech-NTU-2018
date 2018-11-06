def myStrategy(pastData, currPrice):
    #pastData是一群數字 currPrice是當今價格
    import sys
    import numpy as np
    import pandas as pd
    import talib
    #defalut
    action = 0
    bull_bear_index = 0
    # bull = -1
    # bear = 1
    # normal = 0

    comb = np.append(pastData,currPrice)

    #set
    sma_long_day  = 30
    sma_short_day = 5
    rsi_day = 5

    #calculate
    sma_long = (talib.SMA(comb, timeperiod=sma_long_day))[-1]
    sma_short = (talib.SMA(comb, timeperiod=sma_short_day))[-1]
    rsi_current = (talib.RSI(comb, timeperiod=rsi_day))[-1]

    if(sma_long>sma_short):
        bull_bear_index = 1
        #bear
        #長線趨勢高於近期趨勢，代表近期熊
    elif(sma_long<sma_short):
        bull_bear_index = (-1)
        #bull
        #長線趨勢低於近期趨勢，代表近期牛
    else:
        bull_bear_index = 0


    if(bull_bear_index == (-1)):
        #bull
        rsi_high = 60
        rsi_low = 50
        if (rsi_current>=rsi_high):
        #sell
            action = -1
        elif (rsi_current<=rsi_low):
        #buy
            action=1
        else:
        #do nothing
            action=0
    
    elif(bull_bear_index == 1):
        #bear
        rsi_high = 50
        rsi_low = 40
        if (rsi_current>=rsi_high):
        #sell
            action= -1
        elif (rsi_current<=rsi_low):
        #buy
            action=1
        else:
        #do nothing
            action=0
    
    return action