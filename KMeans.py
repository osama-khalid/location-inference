#Generates a csv for words and another for labels where they were max word
from random import shuffle
from datetime import datetime, timedelta
import time 
import numpy as np
import csv
from random import shuffle
from datetime import datetime
import math
import operator

maxWords=open('maxWords_OS_IA_W_0_MX_1_htsPopThreshSubStrict','r').read().split('\n')
allIDs=[]
maxWord={}
AllWords=[]
for row in maxWords:
    if len(row)>0:
        ROW=row.split('|')
        if ROW[0]=='2' or ROW[0]=='1' or ROW[0]=='0':
            allIDs.append(ROW[1])
            
            if ROW[2]==ROW[3]:
                maxWord[ROW[1]]=ROW[4]
                AllWords.append(ROW[4])
                




type=9
Query=open('tweetIA_Hash.csv',"r")          ############
Query=csv.reader(Query, delimiter=',')      ############



Q=[]
for row in Query:
    Q.append(row[:9]+[row[9].lower()]+row[10:])            

t=[]
User={}
Word={}
Locations=[]
for i in range(len(Q)):
    row=Q[i]
    if row[1] in allIDs:
        loc=row[5]
        time=row[3].split(" ")[0]
    
        if time not in t:
            t.append(time)
        #MaxWord list
                
        #Other
        wordlist=row[type].split(",")        
        for q in wordlist:                      #Osama Wrote this back in March 2018, It works so :D
            if q in AllWords:
                if loc not in Locations:
                    Locations.append(loc)
                if q not in Word:
                    Word[q]={}
                if loc not in Word[q]:
                    Word[q][loc]={}
                if time not in Word[q][loc]:
                    Word[q][loc][time]=0
                Word[q][loc][time]=Word[q][loc][time]+1 
            if q not in User:
                User[q]={}
            if time not in User[q]:
                User[q][time]=[]
            
            
            if row[2] not in User[q][time]:
                User[q][time].append(row[2])  

Spatial={}
cells={}
C={}
totInstances={}
for w in Word:
    Spatial[w]={}
    cells[w]=[]
    
    for l in Word[w]:
        Spatial[w][l]=sum(Word[w][l].values())
        cells[w].append(sum(Word[w][l].values()))
    if len(cells[w])>1:
        C[w]=[[x,cells[w].count(x)] for x in set(cells[w])]
    else:
        C[w]=[[1,1]]
    C[w].append([0,len(Locations)-len(Spatial[w])])
    totInstances[w]=sum(Spatial[w].values())
    #Temporal
    

       

hist={}
A=[]
for w in C:
    hist[w]=[]
    for i in C[w]:
        hist[w].append([float(i[0])/float(totInstances[w]),float(i[1])/len(Locations)])
        if float(i[0]) !=0:
            A.append(float(i[0])/float(totInstances[w]))
#Bucketing                    
            
A.sort()
def KMeans(centers,distMatrix,WordSet,k):
    Done=list(set(centers))
    Centeroids={}
    for c in range(k):
        Centeroids[c]=[centers[c]]
    for w in WordSet:  
        if w not in Done:
            Done.append(w)
            Temp=[]
            for c in centers:
                if (c,w) in distMatrix:
                    Temp.append(distMatrix[c,w])
                elif (w,c) in distMatrix:
                    Temp.append(distMatrix[w,c])
            
            Centeroids[Temp.index(min(Temp))].append(w)
    #print(centers)    
    centers=[]    
    for c in Centeroids:
        #print(len(Centeroids[c]))
        AvgDist={}
        for i in range(0,len(Centeroids[c])):
            dist=[]
            for j in range(0,len(Centeroids[c])):
                
                if (Centeroids[c][j],Centeroids[c][i]) in distMatrix:
                    dist.append(distMatrix[Centeroids[c][j],Centeroids[c][i]])
                elif (Centeroids[c][i],Centeroids[c][j]) in distMatrix:
                    dist.append(distMatrix[Centeroids[c][i],Centeroids[c][j]])
                else:
                    dist.append(0)
            AvgDist[Centeroids[c][i]]=float(sum(dist))/len(dist)
        centers.append(sorted(AvgDist.items(),key=operator.itemgetter(1))[0][0])
    return(centers,Centeroids)    
    
def JSD(P,Q):
    DPM=0
    DQM=0
    for i in range(0,len(P)):
        DPM=DPM+P[i]*math.log(0.5*(P[i]+Q[i])/P[i],10)
        DQM=DQM+Q[i]*math.log(0.5*(P[i]+Q[i])/Q[i],10)
    DKL=0.5*DPM+0.5*DQM
    return(-DKL)
    
    
def bucketing(hist,D,A):
    histNorm={}
    WordSet=[]
    for w in hist:
        WordSet.append(w)
        d=float(1)/float(D)
        epsilon=A[0]        
        buckets=np.arange(0.0,1.0,d)
        B={}
        for b in buckets:
            #print(b,math.floor(b*D)/D)
            B[round(b*D)/D]=float(epsilon)/float(D)
        for i in hist[w]:
            #if i[0] ==1.0:
            #    i[0]=i[0]-float(i[0])/float(D)
            B[math.ceil(i[0]*D)/float(D)]=B[math.ceil(i[0]*D)/float(D)]+i[1]
        histNorm[w]=list(B.values())           #To List or not to List
        if D>=100:
            histNorm[w]=list(B.values())[:int(D/10)]+[sum(list(B.values())[int(D/10):])]
        #print(histNorm[w])    
        S=sum(histNorm[w])
        for j in range(0,len(histNorm[w])):
            histNorm[w][j]=histNorm[w][j]/S
    
        
    return(histNorm,WordSet)
d=[10,100,1000]
Cents={}
for D in d: 
    Values=bucketing(hist,D,A)    
    histNorm=Values[0]
    WordSet=Values[1]

    distMatrix={}
    for i in range(0,len(WordSet)):
        for j in range(i+1,len(WordSet)):
            distMatrix[(WordSet[i],WordSet[j])]=JSD(histNorm[WordSet[i]],histNorm[WordSet[j]])
    K=[2,4,10]      
    for k in K:
    #Kmeans 
        shuffle(WordSet)       
        centers=WordSet[:k] 

        for i in range(0,50):
            Values=KMeans(centers,distMatrix,WordSet,k)       
            centers=Values[0]
            centeroids=Values[1]
        Cents[D,k]=Values    
    

    
#Temporal    
Temporal={}
cells={}
C={}
R=3
totInstances={}
for w in Word:
    cells[w]=[]
    Temporal[w]={}
    for time in t:
        Temporal[w][time]=0
    
    
    
    for l in Word[w]:
        for time in Word[w][l]:
            Temporal[w][time]=Temporal[w][time]+Word[w][l][time]
            T=datetime.strptime(time+" 00:00:00", '%Y-%m-%d %H:%M:%S')
            for r in range(1,R+1):
                if (T-timedelta(days=-r)).strftime("%Y-%m-%d %H:%M:%S").split(" ")[0] in t and (T-timedelta(days=-r)).strftime("%Y-%m-%d %H:%M:%S").split(" ")[0] in Word[w][l]:
                    Temporal[w][time]=Temporal[w][time]+Word[w][l][(T-timedelta(days=-r)).strftime("%Y-%m-%d %H:%M:%S").split(" ")[0]]
                    
            for r in range(-1,-R-1,-1):
                if (T-timedelta(days=-r)).strftime("%Y-%m-%d %H:%M:%S").split(" ")[0] in t and (T-timedelta(days=-r)).strftime("%Y-%m-%d %H:%M:%S").split(" ")[0] in Word[w][l]:
                    Temporal[w][time]=Temporal[w][time]+Word[w][l][(T-timedelta(days=-r)).strftime("%Y-%m-%d %H:%M:%S").split(" ")[0]]    
    for time in t:
        cells[w].append(Temporal[w][time])
        
    if len(cells[w])>1:
        C[w]=[[x,cells[w].count(x)] for x in set(cells[w])]
    else:
        C[w]=[[1,1]]
    
    totInstances[w]=sum(Temporal[w].values())
    

hist={}
A=[]
for w in C:
    hist[w]=[]
    for i in C[w]:
        
        hist[w].append([float(i[0])/float(totInstances[w]),float(i[1])/len(t)])
        if float(i[0]) !=0:
            A.append(float(i[0])/float(totInstances[w]))
#Bucketing                    
            
A.sort()       


d=[10,100,1000]
TCents={}
for D in d: 
    Values=bucketing(hist,D,A)    
    histNorm=Values[0]
    WordSet=Values[1]

    distMatrix={}
    for i in range(0,len(WordSet)):
        for j in range(i+1,len(WordSet)):
            distMatrix[(WordSet[i],WordSet[j])]=JSD(histNorm[WordSet[i]],histNorm[WordSet[j]])
    K=[2,3,4,5,6,7,8,9,10]      
    for k in K:
    #Kmeans 
        shuffle(WordSet)       
        centers=WordSet[:k] 

        for i in range(0,50):
            Values=KMeans(centers,distMatrix,WordSet,k)       
            centers=Values[0]
            centeroids=Values[1]
        TCents[D,k]=Values    
    
'''    
for k in K:    
    for y in range(0,k):
        Y=TCents[100,k][1][y]
        Y.sort()
        print(Y)    
    
    print(k)
    
'''    
    
    
    
    
    
    
    
    
    
    
    
    
SpatioTemporal={}
cells={}
C={}
totInstances={}
for w in Word:
    cells[w]=[]
    SpatioTemporal[w]={}
    for time in t:
        for l in Locations:
            SpatioTemporal[w][time,l]=0
        
    
    
    
    for l in Word[w]:
        for time in Word[w][l]:
            SpatioTemporal[w][time,l]=SpatioTemporal[w][time,l]+Word[w][l][time]
    for X in SpatioTemporal[w]:
        cells[w].append(SpatioTemporal[w][X])
        
    if len(cells[w])>1:
        C[w]=[[x,cells[w].count(x)] for x in set(cells[w])]
    else:
        C[w]=[[1,1]]
    
    totInstances[w]=sum(SpatioTemporal[w].values())
    

hist={}
A=[]
for w in C:
    hist[w]=[]
    for i in C[w]:
        hist[w].append([float(i[0])/float(totInstances[w]),float(i[1])/len(t)])
        if float(i[0]) !=0:
            A.append(float(i[0])/float(totInstances[w]))
#Bucketing                    
            
A.sort()       


d=[10,100,1000]
TCents={}
for D in d: 
    Values=bucketing(hist,D,A)    
    histNorm=Values[0]
    WordSet=Values[1]

    distMatrix={}
    for i in range(0,len(WordSet)):
        for j in range(i+1,len(WordSet)):
            distMatrix[(WordSet[i],WordSet[j])]=JSD(histNorm[WordSet[i]],histNorm[WordSet[j]])
    K=[2,3,4,5,6,7,8,9,10]      
    for k in K:
    #Kmeans 
        shuffle(WordSet)       
        centers=WordSet[:k] 

        for i in range(0,50):
            Values=KMeans(centers,distMatrix,WordSet,k)       
            centers=Values[0]
            centeroids=Values[1]
        TCents[D,k]=Values    
    
    
for k in K:    
    for y in range(0,k):
        Y=TCents[100,k][1][y]
        Y.sort()
        print(Y)    
    
    print(k)    