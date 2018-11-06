addpath d:/users/jang/matlab/toolbox/fintech
file='spy.csv';
fprintf('Reading %s...\n', file);
myTable=readtable(file, 'Format', '%s %f %f %f %f %f %f');
adjClose=myTable.AdjClose;

%param=[14, 30, 80];
%tradingFcn=@rsiStrategy;
%figure; returnRate=profitEstimate(adjClose, param, tradingFcn, 1);
%return

lowTh=30;
highTh=80;
windowSizes=[5, 20, 60, 120, 240];
param=[0, lowTh, highTh];
tradingFcn=@rsiStrategy;
for i=1:length(windowSizes)
	param(1)=windowSizes(i);
	figure; returnRate(i)=profitEstimate(adjClose, param, tradingFcn, 1);
end
