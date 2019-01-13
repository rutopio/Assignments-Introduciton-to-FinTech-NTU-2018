addpath d:/users/jang/matlab/toolbox/fintech

%% Read data file
file='spy.csv';
myTable=readtable(file, 'Format', '%s %f %f %f %f %f %f');
adjClose=myTable.AdjClose;
param=[0, 19];
tradingFcn=@myStrategy;
%% Set initial parameters
rate=profitEstimate(adjClose, param, tradingFcn, 1);
fprintf('rate=%g%%\n', rate*100);