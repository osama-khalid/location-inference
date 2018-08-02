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
words=['add', 'bar', 'beer', 'black', 'body', 'book', 'boyfriend', 'brother', 'business', 'coffee', 'county', 'cubs', 'des', 'dogs', 'door', 'double', 'fair', 'field', 'final', 'finish', 'goal', 'green', 'join', 'key', 'ladies', 'lead', 'listening', 'miles', 'national', 'north', 'office', 'park', 'pass', 'photo', 'pick', 'pop', 'power', 'reading', 'ride', 'rock','service', 'share', 'snow', 'social', 'star', 'starts', 'support', 'texas', 'third', 'trump', 'waiting', 'west', 'won','young','7', '8', 'ass', 'bed', 'bet', 'boy', 'boys', 'car', 'care', 'christmas', 'city', 'college', 'country', 'drinking', 'eating', 'fall', 'fan', 'feels', 'fit', 'football', 'free', 'friday', 'fuck', 'fucking', 'full', 'funny', 'gets', 'hell','hit', 'may', 'money', 'music', 'needs', 'ok', 'okay', 'open', 'past', 'pay', 'pizza', 'post', 'red', 'run', 'saturday', 'says', 'season', 'sign', 'sister', 'stay', 'story', 'sunday', 'takes', 'thinking', 'town', 'true', 'use', 'video', 'w', 'wants', 'wear', 'win', 'working','1', '2', '3', '4', '5', 'bad', 'call', 'check', 'even', 'family', 'favorite', 'first', 'friend', 'friends', 'fun', 'game', 'getting', 'girl', 'god', 'guy', 'help', 'high', 'hope', 'house', 'job', 'look', 'looking', 'looks', 'lost', 'lot', 'make', 'making', 'man', 'might', 'miss', 'morning', 'nice', 'nothing', 'oh', 'old', 'person', 'phone', 'play', 'put','read', 'ready', 'say', 'school', 'shit', 'show', 'sleep', 'someone', 'start', 'state', 'stop', 'summer', 'take', 'talk', 'team', 'thing', 'things', 'thought', 'twitter', 'two', 'u', 'us', 'wait', 'watch', 'watching', 'well', 'world', 'wow', 'years', 'yes','amp', 'back', 'best', 'better', 'birthday', 'ca', 'come', 'day', 'feel', 'get', 'go', 'going', 'good', 'great', 'hate', 'home', 'ia', 'iowa', 'know', 'last', 'let', 'life', 'like', 'love', 'much', 'na', 'need', 'night', 'one', 'people', 'right', 'see', 'still', 'thanks', 'think', 'time', 'today', 'tomorrow', 'tonight', 'want', 'way', 'week', 'work', 'year']
Lox=['Fort Madison, IA', 'Oskaloosa, IA', 'North Liberty, IA', 'Altoona, IA', 'Newton, IA', 'Johnston, IA', 'Muscatine, IA', 'Fort Dodge, IA', 'Clinton, IA', 'Mason City, IA', 'Marion, IA', 'Urbandale, IA', 'West Des Moines, IA', 'Ames, IA', 'Iowa City, IA', 'Sioux City, IA', 'Cedar Rapids, IA', 'Des Moines, IA', 'Davenport, IA', 'Waterloo, IA', 'Council Bluffs, IA', 'Dubuque, IA', 'Ankeny, IA', 'Cedar Falls, IA', 'Bettendorf, IA', 'Marshalltown, IA', 'Burlington, IA', 'Ottumwa, IA', 'Coralville, IA', 'Clive, IA', 'Indianola, IA', 'Waukee, IA', 'Boone, IA', 'Spencer, IA', 'Keokuk, IA']
for i in range(len(Q)):
    row=Q[i]
    
    loc=row[5]
    time=row[3].split(" ")[0]
    if datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S')>Cutoff:
        if loc in Lox:
        
                
        #Other
            wordlist=row[type].split(",")        
            for q in wordlist:
                
                if q in words:
                    #print(q)
                    if q not in WordSet:
                        WordSet[q]={}
                    if loc not in WordSet[q]:
                        WordSet[q][loc]=0
                    WordSet[q][loc]=WordSet[q][loc]+1
hist={}                
for q in WordSet:
    hist[q]=[]
    for loc in Lox:
        if loc in WordSet[q]:
            hist[q].append(str(WordSet[q][loc]))
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