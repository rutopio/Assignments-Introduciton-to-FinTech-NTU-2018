import sys
import pandas as pd

filename = sys.argv[1]
df = pd.read_csv(filename,encoding='big5',dtype={'到期月份(週別)' : str,'商品代號' : str})

tx = df[df['商品代號'] == 'TX     ']
tx.reset_index(drop=True, inplace=True)

useful = tx[(tx.成交價格 > 0) & (tx.成交時間>=84500) & (tx.成交時間<=144500) & (tx['到期月份(週別)'] == tx.loc[0,'到期月份(週別)'])]
useful.reset_index(drop=True, inplace=True)

openprice = int(useful.loc[0,'成交價格'])
closeprice = int(useful.loc[len(useful)-1,'成交價格'])
high = int(useful.loc[useful['成交價格'].idxmax(),'成交價格'])
low = int(useful.loc[useful['成交價格'].idxmin(),'成交價格'])

print(openprice,high,low,closeprice)