import sys
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime

filename = './SPY.csv'
df_origin = pd.read_csv(filename)
df_origin = pd.DataFrame(df_origin)
# print(df_origin.head())

def Filter_Data(df):
    
    # 把時間轉成index
    df['Date'] = pd.to_datetime(df['Date'], format = '%Y-%m-%d')
    df = df.set_index(df['Date'],drop=True)
    del df['Date']
    
    df.index = pd.to_datetime(df.index, format = '%Y-%m-%d')
    # print(df)
    return df


def Show_Price_Plot(newdf):
    # 視覺化總價格
    df = newdf['Adj Close']
    df.plot(x=df.index,kind='line')
    plt.show()


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
     

def MACD_Calculate(df):
    # print(df.head())
    macd = pd.DataFrame()
    macd['Date'] = df.index
    
    # 把時間轉成index
    macd['Date'] = pd.to_datetime(macd['Date'], format = '%Y-%m-%d')
    macd = macd.set_index(macd['Date'],drop=True)
    del macd['Date']
    macd.index = pd.to_datetime(macd.index, format = '%Y-%m-%d')

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
    ax2.plot(macd.index, macd['Signal'])

    fig.tight_layout()
    plt.show()
    

df = Filter_Data(df_origin)
# print(df)
# Show_Price_Plot(df)
MACD_Calculate(df)
# RSI_Calculate(df)

