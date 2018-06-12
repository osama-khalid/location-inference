import csv
from datetime import datetime, timedelta
import time 
import threading  
import operator

class NaiveBayes(object):
    def __init__(self,s,t='all',w=0,d=None): 
        ''' s= state e.g. IL, IA, NY 
        t= type i.e. hashtag,noun,all, default=all
        date=the date under consideration, default=all
        w=window
        '''
        self.state=s
        #Cutoff is the empirically<word> derived cutoff date for our experiments.
        #<word> = a placeholder for a term that I can't recall at the moment. Followup: <word> = empirically
        self.Cutoff=datetime.strptime("2016-12-10 02:50:09", '%Y-%m-%d %H:%M:%S')           
        #Reformatting Tweets. 
        output=self.fileOpen(s,t)
        
        self.tweetData=output[0]
        self.folds=self.foldSplit(s)      
        self.date=d
        self.window=w
        self.calendar=output[1]
        
        self.temp={}
        self.temp2={}
        
        
        
    def fileOpen(self,s,t):
        '''
        given a state s, and a type t where type can be either hashtag, noun or both.  
        This takes the raw datadump and generates a nested array (or a table). 
        the 9th (last) column in table is the list of features
        '''
        tweetData=[]
        calendar=[]
        if t=='hashtag':
            print("Generating Data Table for "+s+" with hashtags as features!")
            
            path='data/tweet'+s+'_Hash.csv'
            
            with open(path,'r') as csvfile:   
                readCSV = csv.reader(csvfile, delimiter=',')
                for row in readCSV:    
                    if datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S')>self.Cutoff:
                        calendar.append(row[3].split(' ')[0])
                        tweetData.append([row[0:9]+[row[9].lower()]][0])
        if t=='noun':
            print("Generating Data Table for "+s+" with nouns as features!")
            path='data/tweet'+s+'_Noun.csv'
            with open(path,'r') as csvfile:   
                readCSV = csv.reader(csvfile, delimiter=',')
                for row in readCSV:    
                    if datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S')>self.Cutoff:
                        calendar.append(row[3].split(' ')[0])
                        tweetData.append([row[0:9]+[row[11].lower()]][0])
                
        elif t=='all':
            print("Generating Data Table for "+s+" with nouns+hashtags as features!")
            tweetID=[]
            path='data/tweet'+s+'_Hash.csv'
            with open(path,'r') as csvfile:   
                readCSV = csv.reader(csvfile, delimiter=',')
                for row in readCSV:    
                    if datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S')>self.Cutoff:
                        tweetID.append(row[1])
                        calendar.append(row[3].split(' ')[0])
                        tweetData.append([row[0:9]+[','.join([row[9].lower(),row[11].lower()])]][0])
            path='data/tweet'+s+'_Hash.csv'
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
        #self.temp=trained                  #Debug
        posterior=testing(self.state,i,self.window,maxWord)
        posterior.prediction(i,trained[0],trained[1],self.tweetData,testUser,popDist,maxWord)
                
        
        
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
        
        t={}
        if time !=None:
            for x in time:
                t[x]={}
            t=self.wordSet(userList,data,t,window)        
        else:
            for x in calendar:
                t[x]={}
            t=self.wordSet(userList,data,t,window)        
        return(t)
        
        
    def timeGenerator(self,time,window):
        t=[time]
        time=datetime.strptime(time+" 00:00:00", '%Y-%m-%d %H:%M:%S')
        for w in range(1,window+1):
            t.append((time-timedelta(days=-w)).strftime("%Y-%m-%d %H:%M:%S").split(" ")[0])
        
        for w in range(-1,-window-1,-1):
            t.append((time-timedelta(days=-w)).strftime("%Y-%m-%d %H:%M:%S").split(" ")[0])
        return(t)    
            
    def wordSet(self,users,data,t,window):          #Generates the Set of Words time->city->word->count
        priors={}
        for row in data:
            if row[2] in users:
                city=row[5]
                wordlist=row[-1].split(',')
                time=row[3].split(' ')[0]
                Time=self.timeGenerator(time,window)
                for x in Time:
                    if x in t:
                        if x not in priors:
                            priors[x]={}
                        if city not in priors[x]:
                            priors[x][city]=0
                        priors[x][city]=priors[x][city]+1    
                        if city not in t[x]:
                            t[x][city]={}
                        for w in wordlist:
                            if w not in t[x][city]:
                                t[x][city][w]=0
                            t[x][city][w]=t[x][city][w]+1
        return(t,priors)


class testing(object):
    def __init__(self,state,i,w,maxword):
        j=i
        self.format=open('tweet'+state+'FormatFull').read().split("|")
        self.cities=[]
        for i in range(6,len(self.format)):
            if len(self.format[i])>0:
                self.cities.append(self.format[i])
        self.file=open('Predicted_'+state+"_W_"+str(w)+"_MX_"+str(maxWord)+'.csv'+str(j),'w')
        self.Word=open('Words_'+state+"_W_"+str(w)+"_MX_"+str(maxWord)+'.csv'+str(j),'w')
        
    def prediction(self,i,trained,prior,data,user,popDist,mxW=0,laplacian=1):     #mxW=MaxWords
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
                    for c in trained[time]:
                        likelihood=1
                        featLike={}         #Likelihood of each feature
                        
                        
                        for w in wordlist:
                            if w in trained[time][c]:
                                count=float(trained[time][c][w])
                                
                            else:
                                count=float(0)
                            C=C+count
                            featLike[w]=float(count+laplacian)/float(sum(trained[time][c].values()) + laplacian*len(trained[time]))
                        likelihood=self.maxWords(featLike,mxW)
                        
                            
                        if c in prior[time]:
                            wordCity[c]=likelihood[0]
                            if mxW==0:
                                postPred[c]=likelihood[1]*prior[time][c]
                            else:
                                postPred[c]=likelihood[1]
                            NormFactor=NormFactor+likelihood[1]*prior[time][c]
                           
                        else:
                            wordCity[c]=""
                            postPred[c]=0
                    if C==0:
                        ignore=1
                            
                    prediction=self.normalize(postPred)
                    #ignore=0
                    #if max(prediction.iteritems(), key=operator.itemgetter(1))[1]== min(prediction.iteritems(), key=operator.itemgetter(1))[1]:
                    #    ignore=1
                   
                    #rank=self.eval(prediction,popDist,groundTruth)
                    #print(prediction)
                    #f.write(str(row[1])+','+str(rank)+'\n')
                    self.fileWrite(row,prediction,ignore)
                    self.WordWrite(row,prediction,ignore,wordCity)
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
        
         
    
    def maxWords(self,feature,mxW):
        if mxW == 0:
            wordlist=[]
            posterior=1
            for f in feature:
                posterior=posterior*feature[f]
                wordlist.append(f)
            return(','.join(wordlist),posterior)
        else:
            posterior=1
            wordlist=[]
            sortFeat = sorted(feature.items(), key=operator.itemgetter(1))       #sorted Features
            sortFeat=sortFeat[::-1]
            for i in range(0,min(len(sortFeat),mxW)):
                posterior=sortFeat[i][1]*posterior
                wordlist.append(sortFeat[i][0])
            return(','.join(wordlist),posterior)

    def priorCity(self,prediction):
        return(sorted(prediction.items(), key=operator.itemgetter(1))[::-1][0][0])       #sorted Features  



for i in [0,1,3]:
    for j in [0,1,3]:
        A=NaiveBayes('IA','hashtag',i)#,["2017-10-20"])
        #A.crossValidation()
        maxWord=j
        print("Started for "+str(i)+" Day window and maxwords = "+str(j))
        
        
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

def combine(FILE):
    i=[0,1,3]
    j=[0,1,3]
    k=range(0,10)

    for a in i:
        for b in j:
            A=[]
            for c in k:
                d=open(FILE+"_IA_W_"+str(a)+'_MX_'+str(b)+'.csv'+str(c),'r').read().split("\n")
                shutil.rmtree("Words_IA_W_"+str(a)+'_MX_'+str(b)+'.csv'+str(c))  
                for row in d:
                    if len(row)>0:
                        A.append(row)
                        
            f=open(FILE+"_IA_W_"+str(a)+'_MX_'+str(b)+'.csv','w')
            f.write('\n'.join(A))
            f.close()
        
combine("Words")       
combine("Predicted")     
