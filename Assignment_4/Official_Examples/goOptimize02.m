addpath d:/users/jang/matlab/toolbox/fintech

%% Read data file
file='spy.csv';
fprintf('Reading %s...\n', file);
myTable=readtable(file, 'Format', '%s %f %f %f %f %f %f');
adjClose=myTable.AdjClose;
%% Set initial parameters
alphaVec=-5:25;
betaVec=-5:20;
tradingFcn=@myStrategy;
for i=1:length(alphaVec)
	for j=1:length(betaVec)
		param=[alphaVec(i), betaVec(j)];
		rate(i,j)=profitEstimate(adjClose, param, tradingFcn);
	end
end
rateMax=max(max(rate));
[p, q]=find(rate==rateMax);
p=p(1); q=q(1);
paramBest=[alphaVec(p), betaVec(q)];
fprintf('Max return=%g%%, paramBest=%s\n', 100*rateMax, mat2str(paramBest));
figure;
surf(betaVec, alphaVec, rate); xlabel('beta'); ylabel('alpha'); zlabel('return ratio'); axis tight; box on
%% Plot the whole picture
showPlot=1;
figure;
rate=profitEstimate(adjClose, paramBest, tradingFcn, showPlot);