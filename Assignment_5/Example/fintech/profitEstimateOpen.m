function [returnRate, total]=profitEstimateOpen(priceVec, transFeeRate, actionVec, showPlot)
% profitEstimateOpen: Estimate the profit of a trading strategy, assuming the action is given in advance
%
%	Usage:
%		[returnRate, total]=profitEstimateOpen(priceVec, transFeeRate, actionVec, showPlot)
%
%	Description:
%		[returnRate, total]=profitEstimateOpen(priceVec, transFeeRate, actionVec, showPlot) returns the return rate
%			priceVec: all price info
%			transFeeRate: transaction fee rate
%			actionVec: all actions
%			showPlot: 1 for plotting, 0 for nothing
%			returnRate: return rate
%			total: total asset assuming the initial capital of 1
%
%	Example:
%		file='spy.csv';
%		fprintf('Reading %s...\n', file);
%		myTable=readtable(file, 'Format', '%s %f %f %f %f %f %f');
%		adjClose=myTable.AdjClose;
%		priceVec=myTable.AdjClose;
%		% === Find the optimal actions
%		transFeeRate=0.01;
%		actionVec=myOptimAction(priceVec, transFeeRate);
%		% === Evaluate the actions
%		showPlot=1;
%		[returnRate, total]=profitEstimateOpen(priceVec, transFeeRate, actionVec, showPlot);
%		fprintf('Return rate=%g%%\n', returnRate*100);

%	Roger Jang, 20181028

if nargin<1, selfdemo; return; end
if nargin<2, param=[]; end
if nargin<3, tradingFcn=@maStrategy; end
if nargin<4, showPlot=0; end

%% Parameters and data
capital=1;	% Initial cash
capitalOrig=capital;
%% Start rolling
dataCount=length(priceVec);
suggestedAction=actionVec;	% suggested actions, 1 for buy, -1 for sell
ti=zeros(dataCount,1);	% technical indicator, for example, moving average
stockHolding=zeros(dataCount,1);	% unit of stock in hand
total=zeros(dataCount,1);	% total assets
realAction=zeros(dataCount,1);	% real actions
total(1)=capital;
for i=1:dataCount
	currPrice=priceVec(i);	% Today's price
	if i>1, stockHolding(i)=stockHolding(i-1); end		% Initial holding from yesterday
	switch suggestedAction(i)
		case 1	% "buy"
			if stockHolding(i)==0
				stockHolding(i)=capital*(1-transFeeRate)/currPrice;
				capital=0;
				realAction(i)=1;
			end
		case -1	% "sell"
			if stockHolding(i)>0
				capital=stockHolding(i)*currPrice*(1-transFeeRate);
				stockHolding(i)=0;
				realAction(i)=-1;
			end
		case 0	% Do nothing
		otherwise
			disp('Unknown action!');
	end
	total(i)=capital+stockHolding(i)*currPrice*(1-transFeeRate);
%	fprintf('%d/%d: suggestedAction=%d, stockHolding=%g, capital=%g, realAction=%d, total=%g\n', i, dataCount, suggestedAction(i), stockHolding(i), capital, realAction(i), total(i));
end
returnRate=(total(end)-capitalOrig)/capitalOrig;
%% Plotting
if showPlot
	subplot(311); plot([priceVec, ti], 'linewidth', 1, 'marker', '.');
	title(sprintf('Price, ¡­buy=%d (red), #sell=%d (green)', sum(realAction==1), sum(realAction==-1))); set(gca, 'xlim', [1, dataCount]);
	set(gca, 'xlim', [1, dataCount]);
	axisLimit=axis;
	for i=1:length(realAction)	% Display the real action
		switch(realAction(i))
			case 1
				line(i*[1 1], axisLimit(3:4), 'color', 'r');
			case -1
				line(i*[1 1], axisLimit(3:4), 'color', 'g');
		end
	end
	subplot(312); plot(stockHolding); title('Stock holdings'); set(gca, 'xlim', [1, dataCount]);
	subplot(313); plot(100*(total-capitalOrig)/capitalOrig); title(sprintf('Return rate, final=%g%%', returnRate(end)*100)); set(gca, 'xlim', [1, dataCount]);
	line(axisLimit(1:2), [0 0], 'color', 'r');
	xlabel('Data index'); ylabel('Return rate (%)');
end

% ====== Self demo
function selfdemo
mObj=mFileParse(which(mfilename));
strEval(mObj.example);