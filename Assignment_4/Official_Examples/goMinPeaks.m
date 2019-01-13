addpath d:/users/jang/matlab/toolbox/machineLearning

options = optimset('Display','iter');
options = optimset('Display','iter','PlotFcns',@optimplotfval);
[x,fval,exitflag,output] = fminsearch(@peaksFcn,[0 0],options);