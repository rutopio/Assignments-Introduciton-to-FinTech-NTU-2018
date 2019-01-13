function [action, mv]=maStrategy(pastData, currPrice, window)
%maStrategy: Trading strategy based on moving average

% Roger Jang, 20171126

action=0;
dataLen=length(pastData);
if dataLen<window
	mv=mean(pastData);
	return
end

windowData=pastData(end-window+1:end);
mv=mean(windowData);

if currPrice>mv
	action=1;
elseif currPrice<mv
	action=-1;
end
