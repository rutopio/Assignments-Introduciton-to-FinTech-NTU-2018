import pandas as pd
import numpy as np 
 
import matplotlib.pyplot as plt
 
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score

df = pd.read_csv('./usd_jpy_api.csv')
 
# 最後の 5 行を表示
#print(df.tail())


df['close+1'] = df.close.shift(-1)
df['target'] = df['close+1'] - df['close']
df = df[:-1]

mask1 = df['target'] > 0
mask2 = df['target'] < 0
column_name = 'target'
df.loc[mask1, column_name] = 1
df.loc[mask2, column_name] = 0

df = df[['target','close','open','high','low']]

#print(df.tail())

# 念のため元データから df_2 としてデータを分ける
df_2 = df.copy()
 
# データフレームの行数と列数を取得
n = df_2.shape[0]
p = df_2.shape[1]
 
# データフレームから Numpy 配列へ変換
data = df_2.values
 
# 訓練データ 8 割、テストデータ 2 割へ分割
train_start = 0
train_end = int(np.floor(0.8*n))
test_start = train_end + 1
test_end = n
data_train = data[np.arange(train_start, train_end), :]
data_test = data[np.arange(test_start, test_end), :]
 
# テストデータの最後 2 行を確認
#print(data_test[97:99])

X_train = data_train[:, 1:]
#print(X_train)

y_train = data_train[:, 0]
#print(y_train)

X_test = data_test[:, 1:]
y_test = data_test[:, 0]

print(np.any(np.isnan(X_train)))
print(np.all(np.isfinite(X_train)))

clf = LogisticRegression()
clf.fit(X_train, y_train)


pred_test = clf.predict(X_test)

matrix = confusion_matrix(y_test,pred_test, labels=[0,1])

print(matrix)

 
