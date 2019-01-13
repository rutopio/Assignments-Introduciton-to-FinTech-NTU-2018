% Plot profit vs. windows for RSI (relative strength index)
%	Roger Jang, 20171110, 20180930

clear all
%% Parameters and data
addpath d:/users/jang/matlab/toolbox/fintech
file='spy.csv';
fprintf('Reading %s...\n', file);
myTable=readtable(file, 'Format', '%s %f %f %f %f %f %f');
adjClose=myTable.AdjClose;

windowSizeMax=100;
lowTh=30;
highTh=80;
windowSizes=1:windowSizeMax;
tradingFcn=@rsiStrategy;
param=[0, lowTh, highTh];
for i=1:length(windowSizes)
	param(1)=windowSizes(i);
	returnRate(i)=profitEstimate(adjClose, param, tradingFcn);
%	fprintf('%d/%d: return=%g%%\n', windowSize, windowSizeMax, returnRate(i)*100);
end
%%
figure;
plot(windowSizes, returnRate*100, 'marker', '.'); grid on
xlabel('Window sizes');
ylabel('Return rates (%)');
title('Return rates vs. window sizes for RSI');
[~, index]=max(returnRate);
line(index, returnRate(index)*100, 'color', 'r', 'marker', 'o');
text(index, returnRate(index)*100, sprintf('  [%g, %g%%]', windowSizes(index), returnRate(index)*100));
fprintf('Best window size=%d, max return rate=%g%%\n', index, 100*returnRate(index));
