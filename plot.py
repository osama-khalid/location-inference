import numpy as np
file=open('mwFreq.txt','r').read().split('\n')
Y=[]

X=[]

A={}
B={}
for f in file:
    if len(f)>0:
        row=f.split('|')
        A[row[0]]=float(row[1])
        B[row[0]]=np.round(float(row[2]),5)

B2={}        
A2={}
for b in B:
    if B[b] not in B2:
        B2[B[b]]=0
    B2[B[b]]=B2[B[b]]+A[b]

        
import operator

sortbase=sorted(B.items(),key=operator.itemgetter(1),reverse=True)[::-1]
p=[]
for s in sortbase:
    p.append(s[1])
p=list(set(p))
p.sort()
for s in p:    
    Y.append(B2[s]*float(100))
    X.append(s)
        

from matplotlib import pyplot
from numpy import cumsum
#X2=np.arange(0,len(X))
#X2=X2/float(len(X))
CY=cumsum(Y)
pyplot.plot(X,CY)
pyplot.xlabel('Proportion of Background Words', fontsize=16)
pyplot.ylabel('Percentage of Maxwords', fontsize=16)
pyplot.show()