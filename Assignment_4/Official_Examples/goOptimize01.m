addpath d:/users/jang/matlab/toolbox/fintech

%% Read data file
file='spy.csv';
fprintf('Reading %s...\n', file);
myTable=readtable(file, 'Format', '%s %f %f %f %f %f %f');
adjClose=myTable.AdjClose;
%% Set initial parameters
param0=[10 10];		% alpha & beta
tradingFcn=@myStrategy;
rate0=profitEstimate(adjClose, param0, tradingFcn);
fprintf('param0=%s, rate0=%g%%\n', mat2str(param0), rate0*100);
%% Perform search
options = optimset('Display','iter','PlotFcns',@optimplotfval);
[paramBest, fval, exitflag, output]=fminsearch(@(param) -profitEstimate(adjClose, param, tradingFcn), param0, options);
figure;
rate=profitEstimate(adjClose, paramBest, tradingFcn, 1);	% Compute return rate and plot everything
fprintf('paramBest=%s, rate=%g%%\n', mat2str(paramBest), rate*100);