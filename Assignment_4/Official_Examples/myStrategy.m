function [action, ma]=maStrategy(pastData, currPrice, param)
%maStrategy: Trading strategy based on moving average
%
%	Usage:
%		[action, ma]=myStrategy(pastData, currPrice, param)
%			pastData: historical data
%			currPrice: current (today) price
%			action: 1 for "buy", -1 for "sell", 0 for nothing
%			ma: moving average
%
%	How my strategy is designed:
%		Our technical indicator:
%			Moving average (MA)
%		How the indicator is used:
%			"buy" if currentPrice-alpha>MA
%			"Sell" if currentPrice+beta<MA
%		How many modifiable parameters and what are they
%			3, including window size, alpha, and beta
%		How the system is optimized
%			Window size is fixed at 296, which is obtaind via exhaustive search when [alpha, beta]=[0, 0]
%			Start fminsearch from [alpha, beta]=[10, 10] ==> 153.493% at [8.5 11.25]
%			Use exhaustive search over the range alpha=-5:25 and beta=-5:20 ==> 205.889% at [0, 19]

% Roger Jang, 20181014

if nargin<3||isempty(param)
	param=[0, 19];		% You need to specify param with the best values that you can find in advance.
end

windowSize=296;
alpha=param(1);
beta=param(2);

action=0;
dataLen=length(pastData);
if dataLen<windowSize
	ma=mean(pastData);
	return
end

windowedData=pastData(end-windowSize+1:end);
ma=mean(windowedData);

if currPrice-alpha>ma
	action=1;
elseif currPrice+beta<ma
	action=-1;
end
