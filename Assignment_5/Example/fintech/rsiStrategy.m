function [action, rsi]=rsiStrategy(pastData, currPrice, param)
%rsiStrategy: Trading strategy based on RSI (relative strength index)
%
%	Usage:
%		[action, rsi]=rsiStrategy(pastData, currPrice, param)
%			pastData: historical data
%			currPrice: current (today) price
%			param: parameters for this function
%				param(1): windowSize: window size for computing RSI
%				param(2): low threshold
%				param(3): high threshold
%			action: 1 for "buy", -1 for "sell", 0 for nothing
%			rsi: RSI

% Roger Jang, 20171126

windowSize=param(1); lowTh=param(2); highTh=param(3);
action=0;
dataLen=length(pastData);
if dataLen<windowSize
	priceDiff=pastData(2:end)-pastData(1:end-1);
	up=sum(priceDiff(priceDiff>0));
	down=-sum(priceDiff(priceDiff<0));
	rsi=up/(up+down)*100;
	return
end

windowedData=pastData(end-windowSize+1:end);
priceDiff=windowedData(2:end)-windowedData(1:end-1);
up=sum(priceDiff(priceDiff>0));
down=-sum(priceDiff(priceDiff<0));
rsi=up/(up+down)*100;

if rsi<lowTh
	action=1;
elseif rsi>highTh
	action=-1;
end