### OHLC Extraction

The goal of this homework is to compute the OHLC (open, high, low, close) prices of 台指期 within a given date based on minute-based trading record. The input file is a csv file recording minute-based trading data, which can be download from the following link:

- [前 30 個交易日期貨每筆成交資料](http://www.taifex.com.tw/cht/3/dlFutPrevious30DaysSalesData)

You can download one of the *.csv files and open it with MS Excel to see its contents, which should be self-explanatory. In particular, you should note that

- We should only focus on the 商品代號 of "TX", which is "台指期".
- It is likely that we will have several transactions within a given minute. We can assume all the transactions listed within a given second is based on chronological order. As a result
  - If several transactions occur in the very first minute of the day, then the price of the first transaction within the minute is the "open" price.
  - If several transactions occur in the very last minute of the day, then the price of the last transaction within the minute is the "close" price.
- If you see double dates in 到期月份, please ignore the whole entry directly.

Actually there are more details regarding what we need to do. Please check out this 

You mission is to write a MATLAB function ohlcExtract.m with the following usage:

ohlc=ohlcExtract('input.csv');

where input.csv is the input file of a specific date, while ohlc is a 4-element vector representing the OHLC prices.

For instance, ohlc=ohlcExtract('Daily_2018_08_20.csv') will return a 4-element vector ohlc of "10687 10715 10652 10671".

If you are using Python, then "python3 ohlcExtract.py input.csv" should print out the vector of ohlc in a line, with elements separated by a space.

Here are some test cases:

- Daily_2018_08_20.csv ==> 10687 10715 10652 10671
- Daily_2018_08_31.csv ==> 10975 11024 10953 11022
- Daily_2018_09_28.csv ==> 11011 11039 10921 10955
- Daily_2018_10_01.csv ==> 10968 11018 10966 11006

More hints:

- Judge system

   for you to submit your code. Note that

  - You need to create a new account using your student ID (in lower case), for instance, "r06922119".
  - You should use the registration key "NTU107Fall_CSIE5434FinTech".

- 我們會抓抄襲，分享者和抄襲者都會處罰，請勿以身試法！（上傳別人的程式碼等同抄襲！）

- For MATLAB:

  - MATLAB version: 2018b
  - You can read the csv file like this:myTable=readtable(csvFile,'Format', '%d %s %s %d %f %d %s %s %s');

- For Python:

  - Make sure you specify 'encoding="big5"'.
  - Python version: 3.5.2
  - pandas version: 0.23.4
  - numpy version: 1.14.3