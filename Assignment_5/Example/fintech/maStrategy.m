function [action, ma]=maStrategy(pastData, currPrice, windowSize)
%maStrategy: Trading strategy based on MA (moving average)
%
%	Usage:
%		[action, ma]=maStrategy(pastData, currPrice, windowSize)
%			pastData: historical data
%			currPrice: current (today) price
%			windowSize: window size for computing MA
%			action: 1 for "buy", -1 for "sell", 0 for nothing
%			ma: moving average

% Roger Jang, 20171126

action=0;
dataLen=length(pastData);
if dataLen<windowSize
	ma=mean(pastData);
	return
end

windowedData=pastData(end-windowSize+1:end);
ma=mean(windowedData);

if currPrice>ma
	action=1;
elseif currPrice<ma
	action=-1;
end
