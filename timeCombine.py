import csv
from datetime import datetime, timedelta
import time 
import os
import threading  
import operator

import sys
cities=open('tweetformat','r').read().lower().split('|')
lCut=datetime.strptime("2017-07-01 00:00:00", '%Y-%m-%d %H:%M:%S')           
uCut=datetime.strptime("2017-07-15 00:00:00", '%Y-%m-%d %H:%M:%S')           
type="Noun"
files=['tweetCO_'+type+'.csv','tweetIA_'+type+'.csv','tweetMI_'+type+'.csv','tweetWI_'+type+'.csv','tweetOR_'+type+'.csv']
#files=files[:2]
table=[]
q=0
for f in files:
    with open(f,'r') as csvfile:   
        readCSV = csv.reader(csvfile, delimiter=',')
                
        for row in readCSV:   
            
            if row[5].lower() in cities:
                if datetime.strptime(row[3].split(' ')[0]+' 00:00:00', '%Y-%m-%d %H:%M:%S')>=lCut and datetime.strptime(row[3].split(' ')[0]+' 00:00:00', '%Y-%m-%d %H:%M:%S')<uCut:
                    table.append(row)
                    q=q+1
                    if q%10000==0:
                        print(row)

with open('timeSlice'+type+'.csv', mode='w') as csv_file:
    writer = csv.writer(csv_file,delimiter=',', lineterminator='\n')
    for t in table:
        writer.writerow(t)
        
        
                        