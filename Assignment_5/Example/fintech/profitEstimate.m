function [returnRate, total, ti]=profitEstimate(priceVec, param, tradingFcn, showPlot)
% profitEstimate: Estimate the profit of a trading strategy
%
%	Usage:
%		returnRate=profitEstimate(priceVec, param, showPlot)
%
%	Description:
%		returnRate=profitEstimate(priceVec, param, showPlot) returns the return rate of a trading strategy
%
%	Example:
%		file='spy.csv';
%		fprintf('Reading %s...\n', file);
%		myTable=readtable(file, 'Format', '%s %f %f %f %f %f %f');
%		priceVec=myTable.AdjClose;
%		% For MA
%		param=240;
%		tradingFcn=@maStrategy;
%		figure; returnRate=profitEstimate(priceVec, param, tradingFcn, 1);
%		fprintf('Return rate=%g%%\n', returnRate*100);
%		% For RSI
%		param=[14, 30, 80];
%		tradingFcn=@rsiStrategy;
%		figure; returnRate=profitEstimate(priceVec, param, tradingFcn, 1);
%		fprintf('Return rate=%g%%\n', returnRate*100);

%	Roger Jang, 20171125

if nargin<1, selfdemo; return; end
if nargin<2, param=[]; end
if nargin<3, tradingFcn=@maStrategy; end
if nargin<4, showPlot=0; end

%% Parameters and data
capital=1;	% Initial cash
capitalOrig=capital;
%% Start rolling
dataCount=length(priceVec);
suggestedAction=zeros(dataCount,1);	% suggested actions based on tradingFcn, 1 for buy, -1 for sell
ti=zeros(dataCount,1);	% technical indicator, for example, moving average
stockHolding=zeros(dataCount,1);	% unit of stock in hand
total=zeros(dataCount,1);	% total assets
realAction=zeros(dataCount,1);	% real actions
total(1)=capital;
for i=1:dataCount
	currPrice=priceVec(i);	% Today's price
	[suggestedAction(i), ti(i)]=tradingFcn(priceVec(1:i-1), currPrice, param);	% Suggested action
	if i>1, stockHolding(i)=stockHolding(i-1); end		% Initial holding from yesterday
	switch suggestedAction(i)
		case 1	% "buy"
			if stockHolding(i)==0
				stockHolding(i)=capital/currPrice;
				capital=0;
				realAction(i)=1;
			end
		case -1	% "sell"
			if stockHolding(i)>0
				capital=stockHolding(i)*currPrice;
				stockHolding(i)=0;
				realAction(i)=-1;
			end
		case 0	% Do nothing
		otherwise
			disp('Unknown action!');
	end
	total(i)=capital+stockHolding(i)*currPrice;
%	fprintf('%d/%d: suggestedAction=%d, stockHolding=%g, capital=%g, realAction=%d, total=%g\n', i, dataCount, suggestedAction(i), stockHolding(i), capital, realAction(i), total(i));
end
returnRate=(total(end)-capitalOrig)/capitalOrig;
%% Plotting
if showPlot
	subplot(311); plot([priceVec, ti], 'linewidth', 1, 'marker', '.');
	title(sprintf('Price & technical indicator, param=%s, ¡­buy=%d (red), #sell=%d (green)', mat2str(param), sum(realAction==1), sum(realAction==-1))); set(gca, 'xlim', [1, dataCount]);
	set(gca, 'xlim', [1, dataCount]);
	axisLimit=axis;
	if isequal(tradingFcn, @rsiStrategy)
		lowTh=param(2);
		highTh=param(3);
		line(axisLimit(1:2), highTh*[1 1], 'color', 'r');
		line(axisLimit(1:2), lowTh*[1 1], 'color', 'g');
		hU=text(axisLimit(2), highTh, sprintf('highTh=%g', highTh));
		hD=text(axisLimit(2), lowTh, sprintf('lowTh=%g', lowTh));
	end

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

%	line(axisLimit(1:2), U*[1 1], 'color', 'r');
%	hU=text(axisLimit(2), U, sprintf('U=%g', U));
%	hD=text(axisLimit(2), D, sprintf('D=%g', D));
%	line(axisLimit(1:2), D*[1 1], 'color', 'g');

% ====== Self demo
function selfdemo
mObj=mFileParse(which(mfilename));
strEval(mObj.example);