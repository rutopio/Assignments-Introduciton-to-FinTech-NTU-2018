addpath d:/users/jang/matlab/toolbox/fintech

file='spy.csv';
%%
fprintf('Reading %s via csvread()...\n', file);
num=csvread(file, 1, 1);
adjClose=num(:,5);
%%
fprintf('Reading %s via readtable()...\n', file);
myTable=readtable(file, 'Format', '%s %f %f %f %f %f %f');
adjClose2=myTable.AdjClose;
isequal(adjClose, adjClose2)