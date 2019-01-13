#myStrategy(dailyOhlcvFile,minutelyOhlcvFile,openPricev[evalDays-ic])
 
def myStrategy(daydata, mindata, todayprice):
    # 已知 pastData 是一個 array ，裡面有到今天為止的所有價格，currPrice 是一個數，代表今天的價格。
    import numpy as np
    import talib
  
    day_open = np.array(daydata["open"].values,dtype='f8')
    day_high = np.array(daydata["high"].values,dtype='f8')
    day_low = np.array(daydata["low"].values,dtype='f8')
    day_close = np.array(daydata["close"].values,dtype='f8')
    day_vol = np.array(daydata["volume"].values,dtype='f8')

    # set action as defalut
    action = 0
 
    # 這個是用來判定牛熊的指標
    bull_bear_indicator = 0
    # bear = 1 熊市時設為1
    # bull = -1 熊市時設為2
    # default = 0
 
    # set parameters
    ma_long_day = 30
    ma_short_day = 5
    rsi_day = 5
 
    #MA_Type: 0=SMA, 1=EMA, 2=WMA, 3=DEMA, 4=TEMA, 5=TRIMA, 6=KAMA, 7=MAMA, 8=T3 (Default=SMA)
    ma_long_type = 4
    ma_short_type = 4
 
    bull_rsi_high = 60
    bull_rsi_low = 40
    bear_rsi_high = 50
    bear_rsi_low = 30
 
    # 當下的MA長線值
    ma_long  = (talib.MA(day_close, timeperiod = ma_long_day, matype = ma_long_type))[-1]
    # 當下的MA短線值
    ma_short = (talib.MA(day_close, timeperiod = ma_short_day, matype = ma_short_type))[-1]
    # 當下的RSI值
    rsi_current = (talib.RSI(day_close, timeperiod = rsi_day))[-1]    

    adx = talib.ADX(day_high, day_low, day_close, timeperiod=14)[-1]
    
    #print("ma_long:",ma_long,"ma_short:",ma_short)
    #print("rsi:",rsi_current, "adx: ",adx)

    # 檢查當下是牛市還是熊市
    if (ma_long > ma_short):
        bull_bear_indicator = 1
        # set as bear
        # 近期趨勢走勢低於長期趨勢，視為熊市
    elif (ma_long < ma_short):
        bull_bear_indicator = -1
        # set as bull
        # 近期趨勢走勢高於長期趨勢，視為牛市
    else:
        bull_bear_indicator = 0
 
    # 從RSI判斷買賣
    if (bull_bear_indicator == 1):
        # bear
        if (rsi_current >= bear_rsi_high):
            # sell
            action = -1
        elif (rsi_current <= bear_rsi_low):
            # buy
            action = 1
        else:
            # do nothing
            action = 0
    elif (bull_bear_indicator == -1):
        # bull
        if (rsi_current >= bull_rsi_high):
           # sell
            action = -1
        elif (rsi_current <= bull_rsi_low):
           # buy
            action = 1
        else:
            # do nothing
            action = 0
 
    return action