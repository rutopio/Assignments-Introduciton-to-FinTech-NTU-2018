% Plot profit vs. window sizes for MA (moving average)
%	Roger Jang, 20171110, 20180930

clear all;
%% Parameters and data
addpath d:/users/jang/matlab/toolbox/fintech
file='spy.csv';
fprintf('Reading %s...\n', file);
myTable=readtable(file, 'Format', '%s %f %f %f %f %f %f');
adjClose=myTable.AdjClose;

windowSizeMax=500;
tradingFcn=@maStrategy;
windowSizes=1:windowSizeMax;
for i=1:length(windowSizes)
	windowSize=windowSizes(i);
	returnRate(i)=profitEstimate(adjClose, windowSize, tradingFcn);
%	fprintf('%d/%d: return=%g%%\n', windowSize, windowSizeMax, returnRate(i)*100);
end
%% Plotting
figure;
plot(windowSizes, returnRate*100, 'marker', '.'); grid on
xlabel('Window sizes');
ylabel('Return rates (%)');
title('Return rates vs. window sizes for MA');
[~, index]=max(returnRate);
line(index, returnRate(index)*100, 'color', 'r', 'marker', 'o');
text(index, returnRate(index)*100, sprintf('  [%g, %g%%]', windowSizes(index), returnRate(index)*100));
fprintf('Best windowSize=%d, max return rate=%g%%\n', index, 100*returnRate(index));
axisLimit=axis;
line(5*[1 1], axisLimit(3:4), 'color', 'r');
line(10*[1 1], axisLimit(3:4), 'color', 'r');
line(20*[1 1], axisLimit(3:4), 'color', 'r');
line(60*[1 1], axisLimit(3:4), 'color', 'r');
line(120*[1 1], axisLimit(3:4), 'color', 'r');
line(240*[1 1], axisLimit(3:4), 'color', 'r');
line(480*[1 1], axisLimit(3:4), 'color', 'r');
h=text(5, axisLimit(3), '週線', 'rotation', 90, 'vertical', 'top');
h=text(10, axisLimit(3), '雙週線', 'rotation', 90, 'vertical', 'top');
h=text(20, axisLimit(3), '月線', 'rotation', 90, 'vertical', 'top');
h=text(60, axisLimit(3), '季線', 'rotation', 90, 'vertical', 'top');
h=text(120, axisLimit(3), '半年線', 'rotation', 90, 'vertical', 'top');
h=text(240, axisLimit(3), '年線', 'rotation', 90, 'vertical', 'top');
h=text(480, axisLimit(3), '兩年線', 'rotation', 90, 'vertical', 'top');
