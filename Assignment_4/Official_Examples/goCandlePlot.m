t1=readtable('spy.csv');
t2=table2timetable(t1);
figure; candle(t2);
figure; candle(t2(1:10, :));