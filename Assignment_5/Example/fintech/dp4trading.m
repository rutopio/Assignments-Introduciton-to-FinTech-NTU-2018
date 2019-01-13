%function [return, prev]=dp4trading(priceVec, rho)

m=length(priceVec);
r=zeros(m,3);
s=zeros(m,3);
c=zeros(m,3);
prev=zeros(1,m);
a=1000;		% Initial capital
candidate=zeros(3,1);

%% Initial conditions
% Buy
r(1,1)=a*(1-rho)*(1-rho);
s(1,1)=a*(1-rho)/p(1);
c(1,1)=0;
% Hold
r(1,2)=a;
s(1,2)=0;
c(1,2)=a;
% Sell
r(1,3)=a;
s(1,3)=0;
c(1,3)=a;
%% Recurrent formula
for i=2:m
	% Buy (j=1)
	for j=1:3
		candidate(j)=(s(i-1,j)+c(i-1,j)*(1-rho)/p(i))*p(i)*(1-rho);
	end
	[r(i,1), jHat]=max(candidate);
	s(i,1)=s(i-1,j)+c(i-1,jHat)*(1-rho)/p(i);
	c(i,1)=0;
	prev(i, 1)=jHat;
	% Hold (j=2)
	for j=1:3
		candidate(j)=s(i-1,j)*p(i)*(1-rho)+c(i-1,j);
	end
	[r(i,2), jHat]=max(candidate);
	s(i,2)=s(i-1, jHat);
	c(i,2)=c(i-1, jHat);
	prev(i, 1)=jHat;
	% Sell (j=3)
	for j=1:3
		candidate(j)=s(i-1,j)*p(i)*(1-rho)+c(i-1,j);
	end
	[r(i,3), jHat]=max(candidate);
	s(i,3)=0;
	c(i,3)=r(i, 3);
	prev(i, 1)=jHat;
end
 %% Final answer
