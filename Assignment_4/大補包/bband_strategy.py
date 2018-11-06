def myStrategy(pastData, currPrice):
    #pastData是一群數字 currPrice是當今價格
    import numpy as np
    import pandas as pd
    import talib

    action = 0
    #1買 -1賣
    comb = np.append(pastData,currPrice)

    upper , middle , lower = talib.BBANDS(comb , timeperiod=20, nbdevup=1, nbdevdn=1, matype=2)

    upper_price = upper[-1]
    middle_price = middle[-1]
    lower_price = lower[-1]

    if(currPrice>middle_price)
        action = 1
    elif(currPrice<middle_price)
        action = -1
    
    return action