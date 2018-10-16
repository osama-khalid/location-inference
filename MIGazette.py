from datetime import datetime, timedelta
import time
import os
import csv

ID=0
XX=-1
S="MI"

gzt=[]    
Cutoff=datetime.strptime("2016-12-10 02:50:09", '%Y-%m-%d %H:%M:%S') 
s=S+'_Features_20180801.txt'    
#gzt=open("Gazette.txt",'w')
f= open(s,'r')
T=f.read().split('\n')

for t in range(1,len(T)):

    feats=T[t].split('|')
    if len(feats)>1:
        Name=feats[1].strip()
        Loc=feats[-3]
        if Loc.find("Unknown")==-1:
          
            gzt.append(Name.lower())
            name=Name.replace(" ","")
            if name != Name:
                gzt.append(name.lower())
            
            name=Name.replace(" ","-")
            if name != Name:
                gzt.append(name.lower())
            name=Name.replace(" ","_")
            if name != Name:
                gzt.append(name.lower())
            
print(len(gzt))
gzt=list(set(gzt))
print(len(gzt))
T=[]
x=0
with open("tweet"+S+"_Hash.csv",'r') as csvfile:      #Find Start of targets

    readCSV = csv.reader(csvfile, delimiter=',')
    
    for row in readCSV:
        if datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S')>Cutoff:
            x=x+1
            if x%1000==0:
                    print(x)
            for g in gzt:
                
                if row[4].lower().find(g)>-1:
                    
                    T.append(row[1])
                    break
with open("tweet"+S+"_Noun.csv",'r') as csvfile:      #Find Start of targets

    readCSV = csv.reader(csvfile, delimiter=',')
    
    for row in readCSV:
        if datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S')>Cutoff:
            x=x+1
            if x%1000==0:
                    print(x)
            for g in gzt:
                
                if row[4].lower().find(g)>-1:
                    if row[1] not in T:
                        T.append(row[1])
                    break

                
f=open('Gazette'+S+'.csv','w')
f.write("\n".join(T))
f.close()                
