import pandas as pd
import numpy as np 
 
import matplotlib.pyplot as plt
 
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score

df = pd.read_csv('./^GSPC.csv')
 
# 最後の 5 行を表示
#print(df.tail())


df['close+1'] = df.close.shift(-1)
df['diff'] = df['close+1'] - df['close']
df = df[:-1]
print(df.head())

#上昇と下降の割合を確認する
m = len(df['close'])
#print(len(df[(df['diff'] > 0)]) / m * 100)
#print(len(df[(df['diff'] < 0)]) / m * 100)
 

mask1 = df['diff'] > 0
mask2 = df['diff'] < 0
column_name = 'diff'
df.loc[mask1, column_name] = 1
df.loc[mask2, column_name] = 0
print(df.tail())

print("clean")
df = df[['diff','close','open','high','low','volume','adj close']]

print(df.tail())

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
#print(data_test)



X_train = data_train[:, 1:]
#print(X_train)

y_train = data_train[:, 0]
#print(y_train)

X_test = data_test[:, 1:]
y_test = data_test[:, 0]

#print(np.any(np.isnan(X_train)))
#print(np.all(np.isfinite(X_train)))

clf = LogisticRegression()
clf.fit(X_train, y_train)


pred_test = clf.predict(X_test)

matrix = confusion_matrix(y_test,pred_test, labels=[0,1])

print("Accuracy Matrix:",matrix)

print("Accuracy Rate: ",accuracy_score(y_test,pred_test))


proba_test = clf.predict_proba(X_test)
#print(proba_test[0:5]) 


# 正解ラベルと各クラスの確率をデータフレームへ格納
test_fin = pd.DataFrame({'Actual': y_test,
                         'down_proba': proba_test[:,0],
                         'up_proba' : proba_test[:,1]
                        }, dtype='float64')

#print(test_fin.head(5))

#print("DOWN:",test_fin[test_fin['down_proba'] > 0.56])

#print("UP:",test_fin[test_fin['up_proba'] > 0.56])
