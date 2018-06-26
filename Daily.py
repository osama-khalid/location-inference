import csv
from datetime import datetime, timedelta
import time 
import os
import threading  
import operator
import sys
class NaiveBayes(object):
    def __init__(self,s,t='all',w=0,d=None): 
        ''' s= state e.g. IL, IA, NY 
        t= type i.e. hashtag,noun,all, default=all
        date=the date under consideration, default=all
        w=window
        '''
        self.type=t
        self.state=s
        #Cutoff is the empirically<word> derived cutoff date for our experiments.
        #<word> = a placeholder for a term that I can't recall at the moment. Followup: <word> = empirically
        self.Cutoff=datetime.strptime("2016-12-10 02:50:09", '%Y-%m-%d %H:%M:%S')           
        #Reformatting Tweets. 
        output=self.fileOpen(s,t)
        #output[0]=tweet data
        #output[1]=calendar, all the possible list of days in tweet dataset
        self.tweetData=output[0]
        
        self.folds=self.foldSplit(s)   
        #returns array with n rows x 10 columns, each column=1 fold
        self.date=d
        self.window=w
        self.calendar=output[1]
        
        
    def fileOpen(self,s,t):
        '''
        given a state s, and a type t where type can be either hashtag, noun or both.  
        This takes the raw datadump and generates a nested array (or a table). 
        the 9th (last) column in table is the list of features
        '''
        tweetData=[]
        calendar=[]
        if t=='hashtag':
            print("Generating Data Table for "+s+" with hashtags")
            
            path='data/tweet'+s+'_Hash.csv'
            
            with open(path,'r') as csvfile:   
                readCSV = csv.reader(csvfile, delimiter=',')
                for row in readCSV:    
                    if datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S')>self.Cutoff:
                        calendar.append(row[3].split(' ')[0])
                        tweetData.append([row[0:9]+[row[9].lower()]][0])
        if t=='noun':
            print("Generating Data Table for "+s+" with nouns")
            path='data/tweet'+s+'_Noun.csv'
            with open(path,'r') as csvfile:   
                readCSV = csv.reader(csvfile, delimiter=',')
                for row in readCSV:    
                    if datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S')>self.Cutoff:
                        calendar.append(row[3].split(' ')[0])
                        tweetData.append([row[0:9]+[row[11].lower()]][0])
                
        elif t=='all':
            print("Generating Data Table for "+s+" with nouns+hashtags")
            tweetID=[]
            path='data/tweet'+s+'_Hash.csv'
            with open(path,'r') as csvfile:   
                readCSV = csv.reader(csvfile, delimiter=',')
                for row in readCSV:    
                    if datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S')>self.Cutoff:
                        tweetID.append(row[1])
                        calendar.append(row[3].split(' ')[0])
                        tweetData.append([row[0:9]+[','.join([row[9].lower(),row[11].lower()])]][0])
            path='data/tweet'+s+'_Noun.csv'
            with open(path,'r') as csvfile:   
                readCSV = csv.reader(csvfile, delimiter=',')
                for row in readCSV:    
                    if datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S')>self.Cutoff:
                        if row[1] not in tweetID:
                            calendar.append(row[3].split(' ')[0])
                            tweetData.append([row[0:9]+[','.join([row[9].lower(),row[11].lower()])]][0])
                            
        #Calendar is the list of all dates, from the Cutoff to the most recent                    
        calendar=list(set(calendar))
        calendar.sort()
        print("All Data Loaded")
        return(tweetData,calendar)    

    def foldSplit(self,s):
        '''
        For state s, loads file with the list of users and generates a table where each column represents one of the 10 folds.
        '''
        path='data/folds/Fold'+s+'.csv'
        folds=[[] for i in range(10)]       #10 empty folds
        with open(path,'r') as csvfile:   
            readCSV = csv.reader(csvfile, delimiter=',')
            for row in readCSV:    
                for i in range(0,len(row)):
                    if len(row[i])>0:
                        folds[i].append(row[i])
        print("\nFold Generation Complete\n")
        return(folds)



    def crossValidation(self,i,maxWord):
        '''
        Note: This is one of the most 'dirty' code in this entire implementation.
        Input = i, where i is the fold number.
        This is lazy coding.
        
        I should've made maxWord an input for the __init__ function, 
        but this is an adhoc solution to a different bug caused by the threading. 
        
        
        '''
        testUser=self.folds[i]              #list of test Fold users
        trainUser=[]                        #list of train fold users
        for j in range(0,len(self.folds)):
            if j!=i:
                trainUser=trainUser+self.folds[j]
            
        trainingData=training()             #Initializing the training class!
        print('Fold '+str(i)+" training...")
        trained=trainingData.dataStructure(trainUser,self.tweetData,self.date,self.window,self.calendar)  #
        print('Fold '+str(i)+' Data Structure Generation: Complete')
        popDist=trainingData.popDist(trainUser,self.tweetData)
        
        posterior=testing(self.type,self.state,i,self.window,maxWord)
        posterior.prediction(i,trained[0],trained[1],trained[2],self.tweetData,testUser,popDist,maxWord)
                
        
        
class training(object):  
    def popDist(self,users,data):
        '''
        input= the list of training users, the tweet data table
        output = Dictionary with each city + city population in the training folds
        '''
        popDist={}
        for row in data:
            if row[2] in users:
                city=row[5]
                if city not in popDist:
                    popDist[city]=0
                popDist[city]=popDist[city]+1
        return(popDist)
     

    def dataStructure(self,userList,data,time,window,calendar):
        '''
        input = userList=list of users in training set
                data=tweet data
                window=window size
                calendar = list of all dates
                if time = None, model is trained on all the training tweets after the cutoff 
                    else; model is trained for only the specified date.
        
        '''
        t={}
        if time !=None:
            for x in time:
                t[x]={}                             #t = dictionary of time->city->word->count
            trainedModel=self.wordSet(userList,data,t,window)        
        else:
            for x in calendar:
                t[x]={}
            trainedModel=self.wordSet(userList,data,t,window)        
        return(trainedModel)
        
        
    def timeGenerator(self,time,window):
        '''
            for time t and window w,
            Generates an array of dates centered around a specified t
            ranging between t-w to t+w
        '''
        t=[time]
        time=datetime.strptime(time+" 00:00:00", '%Y-%m-%d %H:%M:%S')
        window=int(window)
        for w in range(1,window+1):
            t.append((time-timedelta(days=-w)).strftime("%Y-%m-%d %H:%M:%S").split(" ")[0])
        
        for w in range(-1,-window-1,-1):
            t.append((time-timedelta(days=-w)).strftime("%Y-%m-%d %H:%M:%S").split(" ")[0])
        return(t)    
            
    def wordSet(self,users,data,t,window):          #dictionary t, time->city->word->count
        '''
        Input = Training UserList, tweet data, dictionary time->city->word->count , and window size
        Output = dictionary time->city->word->count
        prior probability count for time->city->count
        word probability for time->word->probability
        P(city1|tweet) = { P(word1|city1) * P(word2|city1) * P(word3|city1) * P(city1) } / {P(word1) * P(word2) * P(word3) }
        '''
        cityPriors={}                               #dictionary time->city->count                   <- P(city1) from the previous example
        wordPriors={}                               #dictionary time->word->city->count             <- Count(word1),Count(word2),Count(word3) from the previous example
        wordProbs={}                                #dictionary time->word->city->probability       <- P(word1),P(word2),P(word3) from the previous example
        
        for row in data:
            if row[2] in users:
                city=row[5]
                wordlist=row[-1].split(',')
                time=row[3].split(' ')[0]
                Time=self.timeGenerator(time,window)
                for x in Time:
                
                    if x in t:
                        if x not in wordPriors:      
                            wordPriors[x]={}         
                        
                        if x not in cityPriors:
                            cityPriors[x]={}
                        if city not in cityPriors[x]:
                            cityPriors[x][city]=0
                        cityPriors[x][city]=cityPriors[x][city]+1    
                        if city not in t[x]:
                            t[x][city]={}
                        for w in wordlist:
                            if w not in wordPriors[x]:           
                                wordPriors[x][w]={}              
                            if city not in wordPriors[x][w]:        
                                wordPriors[x][w][city]=0            
                            wordPriors[x][w][city]=wordPriors[x][w][city]+1     
                            
                                
                            if w not in t[x][city]:
                                t[x][city][w]=0
                            t[x][city][w]=t[x][city][w]+1
                
        for x in wordPriors:
            if x not in wordProbs:
                wordProbs[x]={}
            for w in wordPriors[x]:
                if w not in wordProbs[x]:
                    wordProbs[x][w]=0               #P(w) = sum( P(C) x P(w|C))
                    
                for c in wordPriors[x][w]:
                    wordProbs[x][w]=wordProbs[x][w]+(float(cityPriors[x][c])/float(sum(cityPriors[x].values())))*(float(wordPriors[x][w][c])/float(sum(wordPriors[x][w].values())))      
        
        
        return(t,cityPriors,wordProbs)


class testing(object):
    def __init__(self,type,state,i,w,maxword):
        part=i
        self.format=open('data/formats/tweet'+state+'FormatFull').read().split("|")
        self.cities=[]
        for i in range(6,len(self.format)):
            if len(self.format[i])>0:
                self.cities.append(self.format[i])
        self.file=open('Predicted_'+state+"_W_"+str(w)+"_MX_"+str(maxWord)+'_'+type+'.csv'+str(part),'w')
        self.Word=open('Words_'+state+"_W_"+str(w)+"_MX_"+str(maxWord)+'_'+type+'.csv'+str(part),'w')
        
    def prediction(self,i,trained,prior,priorWord,data,user,popDist,mxW=0,laplacian=1):     #mxW=MaxWords
        #f=open('temp_'+str(i)+"_"+str(mxW),'w')
        for row in data:
            if row[2] in user:
                postPred={}
                groundTruth=row[5]
                time=row[3].split(' ')[0]        
                wordlist=row[-1].split(',')
                if time in trained:
                    NormFactor=0            #Normalization of likelihood
                    wordCity={}             #Max Word Set in City
                    ignore = 0
                    C=0                     #MetaCount . If all counts for all cities are zero, word doesn't appear in anylocation
                    
                    postPred={}
                    wordCity={}
                    for c in trained[time]:
                        likelihood=1
                        featLike={}         #Likelihood of each feature
                        if c not in postPred:
                            postPred[c]=1
                            wordCity[c]=[]
                        for w in wordlist:
                            
                            if w in trained[time][c]:
                                count=float(trained[time][c][w])
                                C=1
                            else:
                                count=float(0)
                            
                            P=float(count+laplacian)/float(sum(trained[time][c].values()) + laplacian*len(trained[time]))
                            if mxW == 0:
                                postPred[c]=postPred[c]*P
                            else:
                                if w in priorWord[time]:
                                    featLike[w]=P*float(prior[time][c])/float(sum(prior[time].values()))/priorWord[time][w]
                                else:
                                    featLike[w]=P*0.0000001
                        
                        if mxW==0:
                            postPred[c]=postPred[c]*float(prior[time][c])/float(sum(prior[time].values()))
                            wordCity[c]=""
                        else:
                            
                            maxSorting=sorted(featLike.items(),key=operator.itemgetter(1),reverse=True)
                            
                            for i in range(0,min(len(maxSorting),mxW)):
                                
                                postPred[c]=float(maxSorting[i][1])*postPred[c]
                                wordCity[c].append(maxSorting[i][0])
                                
                                
                            
                            wordCity[c]=','.join(wordCity[c])
                    postPred=self.normalize(postPred)
                    #if mxW==0:
                    #    postPred=self.normalize(postPred)
                    #    prediction=[postPred,wordCity]
                    #else:
                    prediction=[postPred,wordCity]
                        
                            
                    #postPred=self.maxWords(likelihood,mxW,priorWord[time],prior[time])   
                    #likelihood[c]=self.maxWords(featLike,mxW,priorWord[time],float(prior[time][c])/float(sum(prior[time].values())))
                        
                            
        
                    if C==0:
                        ignore=1
                            
                    #prediction=self.normalize(postPred)
                    #ignore=0
                    #if max(prediction.iteritems(), key=operator.itemgetter(1))[1]== min(prediction.iteritems(), key=operator.itemgetter(1))[1]:
                    #    ignore=1
                   
                    #rank=self.eval(prediction,popDist,groundTruth)
                    #print(prediction)
                    #f.write(str(row[1])+','+str(rank)+'\n')
                    self.fileWrite(row,prediction[0],ignore)
                    self.WordWrite(row,prediction[0],ignore,prediction[1])
                    #print(float(popDist[prediction[0]])/float(sum(popDist.values())),prediction[1])
                    #if prediction[1]>float(popDist[prediction[0]])/float(sum(popDist.values())):
                    #    print(row[-1],prediction[0],groundTruth)

    
    def WordWrite(self,data,prediction,ignore,wordCity):
        output=[]
        ignoreFlag=str(ignore)
        #print(data)
        TweetId=data[1]
        Handle=data[2]
        GroundTruthCity=data[5]
        Coord=data[6]
        Prior=self.priorCity(prediction)
        output.append(ignoreFlag)
        output.append(TweetId)
        output.append(Handle)
        output.append(GroundTruthCity)
        output.append(Coord)
        output.append(Prior)
        for c in self.cities:
            if c in wordCity:
                #print(wordCity[c],c)
                output.append(wordCity[c])
            else:
                output.append(str(""))
        self.Word.write('|'.join(output)+'\n')
    
                    
    def fileWrite(self,data,prediction,ignore):
        output=[]
        ignoreFlag=str(ignore)
        #print(data)
        TweetId=data[1]
        Handle=data[2]
        GroundTruthCity=data[5]
        Coord=data[6]
        Prior=self.priorCity(prediction)
        output.append(ignoreFlag)
        output.append(TweetId)
        output.append(Handle)
        output.append(GroundTruthCity)
        output.append(Coord)
        output.append(Prior)
        for c in self.cities:
            if c in prediction:
                output.append(str(prediction[c]))
            else:
                output.append(str(0))
        self.file.write('|'.join(output)+'\n')
    
    def normalize(self,likelihood):
        NormFactor=float(sum(likelihood.values()))
        for c in likelihood:
            likelihood[c]=likelihood[c]/NormFactor
        return(likelihood)
        
         
    
  

    def priorCity(self,prediction):
        return(sorted(prediction.items(), key=operator.itemgetter(1))[::-1][0][0])       #sorted Features  



def combine(FILE,type,state,window,maxword):
    a=window
    b=maxword
    k=range(0,10)
    A=[]
    for c in k:
        d=open(FILE+"_"+state+"_W_"+str(a)+'_MX_'+str(b)+'_'+type+'.csv'+str(c),'r').read().split("\n")
        os.remove(FILE+"_"+state+"_W_"+str(a)+'_MX_'+str(b)+'_'+type+'.csv'+str(c))  
        for row in d:
            if len(row)>0:
                A.append(row)
                
    f=open(FILE+"_"+state+"_W_"+str(a)+'_MX_'+str(b)+'_'+type+'.csv','w')
    f.write('\n'.join(A))
    f.close()

if __name__=="__main__":    
    state = str(sys.argv[1])
    type=str(sys.argv[2])
    window=0
    window=int(sys.argv[4])
    maxWord=int(sys.argv[3])
    #type='hashtag'
    #state='IA'
    A=NaiveBayes(state,type,window)#,["2017-10-20"])
    #A.crossValidation()
    j=maxWord
    i=window
    print("\nStarted for "+str(window)+" Day window and maxwords = "+str(j))


    t0 = threading.Thread(target=A.crossValidation,args=(0,maxWord))
    t0.daemon =True
    t0.start()
    t1 = threading.Thread(target=A.crossValidation,args=(1,maxWord))
    t1.daemon =True
    t1.start()
    t2 = threading.Thread(target=A.crossValidation,args=(2,maxWord))
    t2.daemon =True
    t2.start()
    t3= threading.Thread(target=A.crossValidation,args=(3,maxWord))
    t3.daemon =True
    t3.start()
    t4 = threading.Thread(target=A.crossValidation,args=(4,maxWord))
    t4.daemon =True
    t4.start()
    t5 = threading.Thread(target=A.crossValidation,args=(5,maxWord))
    t5.daemon =True
    t5.start()
    t6 = threading.Thread(target=A.crossValidation,args=(6,maxWord))
    t6.daemon =True
    t6.start()
    t7 = threading.Thread(target=A.crossValidation,args=(7,maxWord))
    t7.daemon =True
    t7.start()
    t8 = threading.Thread(target=A.crossValidation,args=(8,maxWord))
    t8.daemon =True
    t8.start()
    t9 = threading.Thread(target=A.crossValidation,args=(9,maxWord))
    t9.daemon =True
    t9.start()

    a=t0.join()
    a=t1.join()
    a=t2.join()
    a=t3.join()
    a=t4.join()
    a=t5.join()
    a=t6.join()
    a=t7.join()
    a=t8.join()
    a=t9.join()


    combine("Words",type,state,window,maxWord)       
    combine("Predicted",type,state,window,maxWord)
