function actionVec=myOptimAction(priceVec, transFeeRate, showPlot)
% myOptimAction: Generate the optimal actions when the price is all known advance
%
%	Usage:
%		actionVec=myOptimAction(priceVec, transFeeRate, showPlot)
%
%	Description:
%		actionVec=myOptimAction(priceVec, transFeeRate, showPlot) returns the optimal actions based on the given price vector and the transaction fee rate.
%
%	Example:
%		file='spy.csv';
%		fprintf('Reading %s...\n', file);
%		myTable=readtable(file, 'Format', '%s %f %f %f %f %f %f');
%		priceVec=myTable.AdjClose;
%		actionVec=myOptimAction(priceVec, 0.01, 1);

%	Roger Jang, 20171125

if nargin<1, selfdemo; return; end
if nargin<2, transFeeRate=0.01; end
if nargin<3, showPlot=0; end

%% Start rolling, with a simple strategy for buy if up for 3 days and sell if down for 3 days
dataCount=length(priceVec);
actionVec=zeros(dataCount, 1);
conCount=3;		% Consecutive counts
for i=1:dataCount
	if i+conCount>dataCount, continue; end
	if all(diff(priceVec(i:i+conCount))>0)	% buy if up for 3 consecutive future days
		actionVec(i)=1;
	end
	if all(diff(priceVec(i:i+conCount))<0)	% Sell if down for 3 consecutive future days
		actionVec(i)=-1;
	end	
end
%% Clean the action vector (since we won't be able to have consecutive "buys" or "sells".)
prevAction=-1;
for i=1:length(actionVec)
%	fprintf('i=%d, prev=%d, act=%d\n', i, prevAction, actionVec(i));
	if actionVec(i)==prevAction
		actionVec(i)=0;
	elseif actionVec(i)==-prevAction
		prevAction=actionVec(i);
	end
%	fprintf('i=%d, prev=%d, act=%d\n', i, prevAction, actionVec(i));
end

%% Plotting
if showPlot
	subplot(111); plot(priceVec, 'linewidth', 1, 'marker', '.');
	title(sprintf('Price, ¡­buy=%d (red), #sell=%d (green)', sum(actionVec==1), sum(actionVec==-1))); set(gca, 'xlim', [1, dataCount]);
	set(gca, 'xlim', [1, dataCount]);
	axisLimit=axis;
	for i=1:length(actionVec)	% Display the real action
		switch(actionVec(i))
			case 1
				line(i*[1 1], axisLimit(3:4), 'color', 'r');
			case -1
				line(i*[1 1], axisLimit(3:4), 'color', 'g');
		end
	end
end

% ====== Self demo
function selfdemo
mObj=mFileParse(which(mfilename));
strEval(mObj.example);