% Plot moving average
%	Roger Jang, 20171110

close all; clear all;
%% Parameters and data
addpath d:/users/jang/matlab/toolbox/fintech
file='spy.csv';
fprintf('Reading %s...\n', file);
myTable=readtable(file, 'Format', '%s %f %f %f %f %f %f');
adjClose=myTable.AdjClose;
plot(adjClose);
windows=[5, 10, 20, 60, 120, 240];
for i=1:length(windows)
	window=windows(i);
	lineSet(:,i)=nanmean(enframe([nan*ones(window-1,1); adjClose], window, window-1))';
end
%% Plot of all data
plot([adjClose, lineSet]);
legend({'Price', '週線', '雙週線', '月線', '季線', '半年線', '年線'}, 'location', 'northOutside', 'orientation', 'horizontal');
axis tight
start=1; stop=length(adjClose);
set(gca, 'xlim', [start stop]);
title(sprintf('10-year (global) view (from %d to %d)', start, stop)); xlabel('Data index'); ylabel('Price');
%% Zoom in to 1-year view
figure;
plot([adjClose, lineSet]);
legend({'Price', '週線', '雙週線', '月線', '季線', '半年線', '年線'}, 'location', 'northOutside', 'orientation', 'horizontal');
axis tight
start=1020; stop=start+240-1;
set(gca, 'xlim', [start stop]);
h=findobj(gca, 'type', 'line'); set(h, 'marker', '.');
title(sprintf('1-year view (from %d to %d)', start, stop)); xlabel('Data index');
%% Zoom in 1-quarter view
figure;
plot([adjClose, lineSet]);
legend({'Price', '週線', '雙週線', '月線', '季線', '半年線', '年線'}, 'location', 'northOutside', 'orientation', 'horizontal');
axis tight
start=1020; stop=start+60-1;
set(gca, 'xlim', [start stop]);
h=findobj(gca, 'type', 'line'); set(h, 'marker', '.');
title(sprintf('1-quarter view (from %d to %d)', start, stop)); xlabel('Data index');