def myStrategy(pastData, currPrice):
    import numpy as np
    param=[0, 19]
    windowSize=296
    alpha=param[0]
    beta=param[1]
    action=0
    dataLen = len(pastData)
    if dataLen<windowSize:
        ma=np.mean(pastData)
        return 0
    windowedData=pastData[-windowSize:]
    ma=np.mean(windowedData)
    if (currPrice-alpha)>ma:
        action=1
    elif (currPrice+beta)<ma:
        action=-1
    else:
        action=0
    return action
