addpath d:/users/jang/matlab/toolbox/fintech
%% Read data
file='spy.csv';
fprintf('Reading %s...\n', file);
myTable=readtable(file, 'Format', '%s %f %f %f %f %f %f');
adjClose=myTable.AdjClose;
%% Perform test
windowSizes=[5, 20, 60, 120, 240];
tradingFcn=@maStrategy;
for i=1:length(windowSizes)
	figure; returnRate(i)=profitEstimate(adjClose, windowSizes(i), tradingFcn, 1);
end

