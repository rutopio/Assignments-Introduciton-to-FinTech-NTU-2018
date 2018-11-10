import sys
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import talib

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score


filename = './SPY.csv'
df_origin = pd.read_csv(filename)
df_origin = pd.DataFrame(df_origin)
# print(df_origin.head())

def Datatime_Trans(df):
    df['Date'] = pd.to_datetime(df['Date'], format = '%Y-%m-%d')
    df = df.set_index(df['Date'],drop=True)
    df.index = pd.to_datetime(df.index, format = '%Y-%m-%d')
    del df['Date']
    return df

def Show_Price_Plot(newdf):
    # 視覺化總價格
    df = newdf['Adj Close']
    df.plot(x=df.index,kind='line',grid=TRUE)
    plt.show()


def SMA(df):

    sma = pd.DataFrame()
    
    sma['Date'] = df.index
    sma = Datatime_Trans(sma)
    sma['Close'] = df['Adj Close']
    sma['SMA_5'] = np.round(sma['Close'].rolling(window=5).mean(),2)
    sma['SMA_15'] = np.round(sma['Close'].rolling(window=15).mean(),2)
    
    #sma[['Close','SMA_5','SMA_15']].plot()
    #plt.show()
    #求長短線之差
    sma['Diff'] = sma['SMA_5'] - sma['SMA_15']
    #print(sma.tail())

    #求黃金交叉
    asign = np.sign(sma['Diff'])

    sz = asign == 0
    while sz.any():
        asign[sz] = np.roll(asign,1)[sz]
        sz = asign == 0

    signchange = ((np.roll(asign,1)-asign)==-2).astype(int)
    sma['Cross'] = signchange
    sma['Golden'] = sma['Cross']

    # 求死亡交叉

    asign = np.sign(sma['Diff'])

    sz = asign == 0
    while sz.any():
        asign[sz] = np.roll(asign,1)[sz]
        sz = asign == 0

    signchange = ((np.roll(asign,1)-asign)==2).astype(int)
    sma['Cross'] = signchange
    sma['Dead'] = sma['Cross']
    sma.loc[sma['Dead']==1,'Dead'] = -1  #WTF

    # 檢查兩個交叉是否相同數量

    print(sma[['Golden','Dead']])
    # print(sma['dead'].sum())

    # SMA決策
    sma['Return'] = sma['Close'] - sma['Close'].shift(1)
    sma['Golden_profit'] = sma['Return'] * sma['Golden'].shift(1)
    sma['Dead_profit'] = sma['Return'] * sma['Dead'].shift(1)
    del sma['Cross']   

    sma[['Golden','Dead']].cumsum().plot(grid=True)
    
    print(np.cumsum(sma['Golden_profit']))
    print(np.cumsum(sma['Dead_profit']))


    gprof = np.cumsum(sma['Golden_profit']).values

    n = len(gprof)
    #print(n)
    #print(gprof[n-1])

    fig, (ax1, ax2) = plt.subplots(2,1)
    ax1.plot(sma.index, sma['Close'])
    ax1.plot(sma.index, sma['SMA_5'])
    ax1.plot(sma.index, sma['SMA_15'])
    ax2.plot(sma.index, sma['Golden_profit'].cumsum())
    ax2.plot(sma.index, sma['Dead_profit'].cumsum())

    # fig.tight_layout()
    #print(sma[['SMA_5','SMA_15','Golden_profit','Dead_profit']])

    plt.show()
    

    return sma

def RSI_Calculate(newdf):

    
    df = newdf['Adj Close']

    diff = df.diff()
    up = diff.copy()
    down = diff.copy()
    
    up[up<0] = 0
    down[down>0] = 0
    
    # 以14天為周期
    up_sma_14 = up.rolling(window=14, center = False).mean()
    down_sma_14 = down.abs().rolling(window = 14,center = False).mean()
    

    RS = up_sma_14/down_sma_14
    RSI = 100 - (100/(1+RS))
    # 輸出RSI
    # print(RSI)
    
    # 畫圖
    fig, (ax1,ax2) = plt.subplots(2,1,gridspec_kw = {'height_ratios':[3,1]})

    ax1.plot(df.index,df)
    ax2.plot(RSI.index,RSI)
    
    fig.tight_layout()
    plt.show()

    return RSI
     
def MACD_Calculate(df):
    # print(df.head())
    macd = pd.DataFrame()

    macd['Date'] = df.index
    
    macd = Datatime_Trans(macd)

    macd['Close'] = df['Adj Close']
    # print(macd['Close'].head())
    macd['EMA_12'] = df['Adj Close'].ewm(span=12).mean()
    macd['EMA_26'] = df['Adj Close'].ewm(span=26).mean()
    macd['MACD'] = macd['EMA_12'] - macd['EMA_26']
    macd['Signal'] = macd['MACD'].ewm(span=9).mean()
    print(macd.head())

    fig, (ax1, ax2) = plt.subplots(2,1,gridspec_kw = {'height_ratios':[3,1]})
    ax1.plot(macd.index, macd['Close'])
    ax2.plot(macd.index, macd['MACD'])
    #ax2.plot(macd.index, macd['Signal'])

    fig.tight_layout()
    plt.show()

    return macd

def Bollband(df):
    bband = pd.DataFrame()
    bband['Date'] = df.index
    
    bband = Datatime_Trans(bband)

    bband['Close'] = df['Adj Close']

    bband['Mean'] = df['Adj Close'].rolling(window=20).mean()
    bband['Std'] = df['Adj Close'].rolling(window=20).std()
    bband['Upper'] = bband['Mean'] + (2*bband['Std'])
    bband['Lower'] = bband['Mean'] - (2*bband['Std'])
    print(bband)

    bband[['Close','Mean','Upper','Lower']].plot()
    plt.show()


def EMA(df):
    ema = pd.DataFrame()
    ema['Date'] = df.index
    ema = Datatime_Trans(ema)

    ema['Close'] = df['Adj Close']

    ema['EMA_26'] = ema['Close'].ewm(span=26).mean()
    ema['EMA_9'] = ema['Close'].ewm(span=9).mean()
    print(ema)
    ema[['EMA_26','EMA_9']].plot()
    plt.show()


def FX(df):
    df = df.reset_index()
    #df = df.round(3)

    df['Close+1'] = df['Close'].shift(-1)
    df['Diff'] = df['Close+1'] - df['Close']
    df = df[:-1]

    #print(df.head())
    
    #割合檢查
    #m = len(df['Close'])
    #print(len(df[(df['Diff']>0)])/m*100)
    #print(len(df[(df['Diff']<0)])/m*100)

    
    df.loc[df['Diff']>0,'Target'] = 1
    df.loc[df['Diff']<=0,'Target'] = 0
    

    #df = df[['Target','Adj Close','Open','High','Low']]
    df = df[['Target','Adj Close']]
    
    #print(df.isnull().sum())

    df_2 = df.copy()
    df_2.fillna(0)
    # データフレームから Numpy 配列へ変換    
    data = df_2.values
    #data = data.round(2)
    np.set_printoptions(suppress=True) 
    
    #print(data)    

    n = df_2.shape[0]
    p = df_2.shape[1]
       
    train_start = 0
    train_end = int(np.floor(0.5*n))
    test_start = train_end + 1
    test_end = n
    data_train = data[np.arange(train_start, train_end), :]
    data_test = data[np.arange(test_start, test_end), :]
    
    #print(data_test[97:99])

    X_train = data_train[:, 1:]
    y_train = data_train[:, 0]
    #print(X_train)
    #print(y_train)
    X_test = data_test[:, 1:]
    y_test = data_test[:, 0]
    np.set_printoptions(suppress=True) 
    
    #print(np.any(np.isnan(X_train)))
    #print(np.all(np.isfinite(X_train)))
    
    # Model train
        
    clf = LogisticRegression()
    clf.fit(X_train, y_train)
    
    LogisticRegression(C=1.0, class_weight=None, dual=False, fit_intercept=True,
          intercept_scaling=1, max_iter=100, multi_class='ovr', n_jobs=1,
          penalty='l2', random_state=None, solver='liblinear', tol=0.0001,
          verbose=0, warm_start=False)
    
    #預測
     
    pred_test = clf.predict(X_test)

    matrix = confusion_matrix(y_test,pred_test, labels=[0,1])

    print("matrix rate: " , matrix)

    print("Acc Score: ",accuracy_score(y_test,pred_test))

    proba_test = clf.predict_proba(X_test)

    test_fin = pd.DataFrame({'Actual': y_test,
                         'down_proba': proba_test[:,0],
                         'up_proba' : proba_test[:,1]
                        }, dtype='float64')

    #print(test_fin.head(10))
    print("Down_prob : ",test_fin[test_fin['down_proba'] > 0.54])

    print("Up_Prob : ",test_fin[test_fin['up_proba'] > 0.54])
    
    fig, (ax1, ax2) = plt.subplots(2,1, gridspec_kw = {'height_ratios':[3, 1]})
    ax1.plot(df['Adj Close'][400:500].index, df['Adj Close'][400:500])
    ax1.axvline(x = 412, color='red', linewidth=0.8, alpha=0.5)
    ax1.axvline(x = 429, color='red', linewidth=0.8, alpha=0.5)
    ax1.axvline(x = 442, color='red', linewidth=0.8, alpha=0.5)
    ax1.axvline(x = 456, color='red', linewidth=0.8, alpha=0.5)
    ax1.axvline(x = 460, color='red', linewidth=0.8, alpha=0.5)
    ax2.plot(test_fin['up_proba'].index, test_fin['up_proba'])
    ax2.axhline(y = 0.5, color='green', linewidth=0.8, alpha=0.5)
    ax2.axvline(x = 12, color='red', linewidth=0.8, alpha=0.5)
    ax2.axvline(x = 29, color='red', linewidth=0.8, alpha=0.5)
    ax2.axvline(x = 42, color='red', linewidth=0.8, alpha=0.5)
    ax2.axvline(x = 56, color='red', linewidth=0.8, alpha=0.5)
    ax2.axvline(x = 60, color='red', linewidth=0.8, alpha=0.5)
    plt.legend()
    #plt.show()
    

df = Datatime_Trans(df_origin)

FX(df)
#EMA(df)
# print(df)
#SMA(df)
# Show_Price_Plot(df)
#MACD_Calculate(df)
#RSI_Calculate(df)
# Bollband(df)

