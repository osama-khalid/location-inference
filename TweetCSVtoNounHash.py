import csv
from nltk import word_tokenize as WT
import string
from nltk.corpus import wordnet as wn
from nltk.corpus.reader import NOUN
A=[]


stopwords=['i', 'me', 'my', 'http', 'https', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now']    

i=0    
with open("tweet2TX.csv") as csvfile:      #Find Start of targets

    readCSV = csv.reader(csvfile, delimiter=',')
    
    for row in readCSV:
        
        
        if len(row)<11:
            row.append([0])
            row.append([0])
        if len(row[9])>0:
            row[8]=1
        else:
            row[8]=0
        
        tweets=row[4].lower().split()
        punctuations=list(string.punctuation)
        
        tweet=[]
        for t in tweets:
            if t[0]!='#':
                tweet.append(t)
        tweets=' '.join(tweet)        
        wordlist=[]
    
        tweets=[i for i in WT(tweets) if i not in punctuations]
        for tweet in tweets:
            if len(wn.synsets(tweet,NOUN)) > 0 and tweet.lower().strip() not in stopwords:
                wordlist.append(tweet)            
        wordlist=','.join(wordlist)
        if len(wordlist)>0:
            row[10]=1
        if len(wordlist)==0:
            row[10]=0 
        row[11]=wordlist
        A.append(row)
        
        
with open("tweetTX.csv") as csvfile:      #Find Start of targets

    readCSV = csv.reader(csvfile, delimiter=',')
    
    for row in readCSV:
        
        
        if len(row)<11:
            row.append([0])
            row.append([0])
        if len(row[9])>0:
            row[8]=1
        else:
            row[8]=0
        
        tweets=row[4].lower().split()
        punctuations=list(string.punctuation)
        
        tweet=[]
        for t in tweets:
            if t[0]!='#':
                tweet.append(t)
        tweets=' '.join(tweet)        
        wordlist=[]
    
        tweets=[i for i in WT(tweets) if i not in punctuations]
        for tweet in tweets:
            if len(wn.synsets(tweet,NOUN)) > 0 and tweet.lower().strip() not in stopwords:
                wordlist.append(tweet)            
        wordlist=','.join(wordlist)
        if len(wordlist)>0:
            row[10]=1
        if len(wordlist)==0:
            row[10]=0 
        row[11]=wordlist
        A.append(row)        
        
        
with open("tweetTX_Hash.csv", "w") as csv_file:
    writer=csv.writer(csv_file,delimiter=',', lineterminator='\n')
    j=0
    for r in A:
        if len(r[9])>1:
            writer.writerow(r)         
            
with open("tweetTX_Noun.csv", "w") as csv_file:
    writer=csv.writer(csv_file,delimiter=',', lineterminator='\n')
    j=0
    for r in A:
        if len(r[11])>1:
            writer.writerow(r)                     