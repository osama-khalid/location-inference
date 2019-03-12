file=open('mwFreq.txt','r').read().split('\n')
Y=[]
X=[]
for f in file:
    if len(f)>0:
        row=f.split('|')
        X.append(float(row[1])*100)
        Y.append(float(row[2])*100)
        
import numpy as np
from matplotlib import pyplot
from numpy import cumsum
X2=np.arange(0,len(file)-1)
CY=cumsum(Y)
pyplot.plot(X2,CY)
pyplot.xlabel('Number of Unique MaxWords', fontsize=16)
pyplot.ylabel('Percentage of Background Words Covered', fontsize=16)
pyplot.show()