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



type=11
Query=open('tweetIA_Noun.csv',"r")          ############
Query=csv.reader(Query, delimiter=',')      ############



Q=[]
for row in Query:
    Q.append(row)            
Cutoff=datetime.strptime("2016-12-10 02:50:09", '%Y-%m-%d %H:%M:%S')           
#Reformatting Tweets. 
t=[]
User={}
WordSet={}
Locations=[]
words=['action', 'add', 'boyfriend', 'brewing', 'business', 'chicago', 'chill', 'd', 'dogs', 'door', 'dying', 'east', 'fair','falls', 'field', 'finish', 'fit', 'goal', 'goals', 'green', 'hawks', 'health', 'history', 'key', 'lane', 'lets', 'movies', 'pass', 'power', 'reading', 'ride', 'rock', 'score', 'service', 'share', 'shirt', 'sign', 'snow', 'social', 'solid', 'south', 'star', 'starts', 'step', 'stout', 'students', 'tap', 'track', 'wins','2', '3', 'bad', 'better', 'come', 'drinking', 'even', 'feel', 'first', 'friends', 'fuck', 'game', 'getting', 'girl', 'hate', 'home', 'hope', 'last', 'let', 'look', 'man', 'miss', 'oh', 'say', 'shit', 'take', 'thanks', 'thing', 'things', 'tomorrow', 'two', 'u', 'us', 'wait', 'watch', 'way', 'week', 'well', 'year','amp', 'back', 'best', 'birthday', 'ca', 'day', 'get', 'go', 'going', 'good', 'great', 'ia', 'iowa', 'know', 'life', 'like', 'love', 'make', 'much', 'na', 'need', 'night', 'one', 'people', 'right', 'see', 'someone', 'still', 'think', 'time', 'today', 'tonight', 'want', 'work','7', '8', 'bar', 'beer', 'black', 'boy', 'boys', 'car', 'care', 'check', 'clear', 'coffee', 'college', 'country', 'current', 'des', 'fall', 'family', 'fan', 'feels', 'football', 'free', 'friday', 'full', 'funny', 'gets', 'hell', 'hit', 'lost', 'making', 'may', 'money', 'music', 'needs', 'ok', 'okay', 'open', 'park', 'phone', 'read', 'run', 'saturday', 'says', 'stay', 'story', 'summer', 'thinking', 'true', 'trump', 'twitter', 'use', 'video', 'w', 'wants', 'working','1', '4', '5', 'ass', 'bed', 'call', 'city', 'favorite', 'friend', 'fucking', 'fun', 'god', 'guy', 'help', 'high', 'house', 'job', 'looking', 'looks', 'lot', 'might', 'morning', 'nice', 'nothing', 'old', 'person', 'play', 'put', 'ready', 'school', 'season', 'show', 'sleep', 'start', 'state', 'stop', 'talk', 'team', 'thought', 'watching', 'win', 'world', 'wow', 'years', 'yes']

for i in range(len(Q)):
    row=Q[i]
    
    loc=row[5]
    time=row[3].split(" ")[0]
    if datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S')>Cutoff:
        #print(time)
        if time not in t:
            t.append(time)
        #MaxWord list
                
        #Other
        wordlist=row[type].split(",")        
        for q in wordlist:
            
            if q in words:
                #print(q)
                if q not in WordSet:
                    WordSet[q]={}
                if time not in WordSet[q]:
                    WordSet[q][time]=0
                WordSet[q][time]=WordSet[q][time]+1
hist={}                
for q in WordSet:
    hist[q]=[]
    for time in t:
        if time in WordSet[q]:
            hist[q].append(str(WordSet[q][time]))
            #print(q,time,WordSet[q][time])
        else:
            hist[q].append(str(0))
#    for q in wordlist:                      #Osama Wrote this back in March 2018, It works so :D
X=open("_location",'w')

    
for q in hist:
    X.write(q+'\n')
    f=open(q,'w')
    f.write(','.join(hist[q]))
    f.close()