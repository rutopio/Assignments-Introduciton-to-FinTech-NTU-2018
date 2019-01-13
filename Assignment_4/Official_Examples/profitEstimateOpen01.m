addpath d:/users/jang/matlab/toolbox/fintech

%% Read data
file='spy.csv';
fprintf('Reading %s...\n', file);
myTable=readtable(file, 'Format', '%s %f %f %f %f %f %f');
adjClose=myTable.AdjClose;
priceVec=myTable.AdjClose;
%% Find the optimal actions
transFeeRate=0.01;		% Typical transaction fee rate is 1%.
actionVec=myOptimAction(priceVec, transFeeRate);
%% Evaluate the actions
showPlot=1;
[returnRate, total]=profitEstimateOpen(priceVec, transFeeRate, actionVec, showPlot);