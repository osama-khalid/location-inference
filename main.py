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
        self.Cutoff=datetime.strptime("2016-12-10 02:50:09", '%Y-%m-%d %H:%M:%S')
        output=self.fileOpen(s,t)
        self.tweetData=output[0]
        self.folds=self.foldSplit(s)      #folds
        self.date=d
        self.window=w
        self.calendar=output[1]
        #Temp
        self.temp={}
        self.temp2={}
        
        
        
    def fileOpen(self,s,t):
        tweetData=[]
        calendar=[]
        if t=='hashtag':
            print(1)
            
            path='data/tweet'+s+'_Hash.csv'
            
            with open(path,'r') as csvfile:   

                readCSV = csv.reader(csvfile, delimiter=',')
    
                for row in readCSV:    
                    if datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S')>self.Cutoff:
                        #tweetid,userid,date,groundtruthcity,hash/noun
                        
                        calendar.append(row[3].split(' ')[0])
                        tweetData.append([row[0:9]+[row[9].lower()]][0])
            
        
        if t=='noun':
            print(2)
            path='data/tweet'+s+'_Noun.csv'
            with open(path,'r') as csvfile:   

                readCSV = csv.reader(csvfile, delimiter=',')
        
                for row in readCSV:    
                    if datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S')>self.Cutoff:
                        #tweetid,userid,date,groundtruthcity,hash/noun
                        calendar.append(row[3].split(' ')[0])
                        tweetData.append([row[0:9]+[row[11].lower()]][0])
                
        
        elif t=='all':
            print(3)
            tweetID=[]
            
            path='data/tweet'+s+'_Hash.csv'
            with open(path,'r') as csvfile:   

                readCSV = csv.reader(csvfile, delimiter=',')
        
                for row in readCSV:    
                    if datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S')>self.Cutoff:
                        #tweetid,userid,date,groundtruthcity,hash/noun
                        tweetID.append(row[1])
                        calendar.append(row[3].split(' ')[0])
                        tweetData.append([row[0:9]+[','.join([row[9].lower(),row[11].lower()])]][0])
                
            path='data/tweet'+s+'_Hash.csv'
            with open(path,'r') as csvfile:   

                readCSV = csv.reader(csvfile, delimiter=',')
        
                for row in readCSV:    
                    if datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S')>self.Cutoff:
                        #tweetid,userid,date,groundtruthcity,hash/noun
                        if row[1] not in tweetID:
                            calendar.append(row[3].split(' ')[0])
                            tweetData.append([row[0:9]+[','.join([row[9].lower(),row[11].lower()])]][0])
        calendar=list(set(calendar))
        calendar.sort()
        
        
        
        print("All Data Loaded")
        return(tweetData,calendar)    
        
        
    def foldSplit(self,s):
        path='data/folds/Fold'+s+'.csv'
        folds=[[] for i in range(10)]       #10 empty folds
        with open(path,'r') as csvfile:   

            readCSV = csv.reader(csvfile, delimiter=',')
            
            for row in readCSV:    
                for i in range(0,len(row)):
                    if len(row[i])>0:
                        folds[i].append(row[i])
            
        print("Fold Generation Complete")
        return(folds)



    def crossValidation(self,i,j):
        
        testUser=self.folds[i]              #list of test Fold users
        trainUser=[]                        #list of train fold users
        for j in range(0,len(self.folds)):
            if j!=i:
                trainUser=trainUser+self.folds[j]
            
        trainingData=training()
        print('Fold '+str(i)+":")
        trained=trainingData.dataStructure(trainUser,self.tweetData,self.date,self.window,self.calendar)
        popDist=trainingData.popDist(trainUser,self.tweetData)
        self.temp=trained
        posterior=testing(self.state,i,self.window)
        posterior.prediction(trained[0],trained[1],self.tweetData,testUser,popDist)
        #self.temp2=
        
        
class testing(object):
    def __init__(self,state,i,w):
        j=i
        self.format=open('tweet'+state+'FormatFull').read().split("|")
        self.cities=[]
        for i in range(6,len(self.format)):
            if len(self.format[i])>0:
                self.cities.append(self.format[i])
            
        
        self.file=open('Predicted_'+state+"_"+str(w)+"_"+str(0)+'.csv'+str(j),'w')
        
    def prediction(self,trained,prior,data,user,popDist,mxW=0,laplacian=1):     #mxW=MaxWords
        
        for row in data:
            if row[2] in user:
                
                postPred={}
                
                groundTruth=row[5]
                time=row[3].split(' ')[0]        
                wordlist=row[-1].split(',')
                if time in trained:
                    NormFactor=0            #Normalization of likelihood
                    wordCity={}             #Max Word Set in City
                    for c in trained[time]:
                        likelihood=1
                        featLike={}         #Likelihood of each feature
                        for w in wordlist:
                            if w in trained[time][c]:
                                count=float(trained[time][c][w])
                            else:
                                count=float(0)
                            
                            featLike[w]=float(count+laplacian)/float(sum(trained[time][c].values()) + laplacian*len(trained[time]))
                            
                        likelihood=self.maxWords(featLike,mxW)
                        
                        if c in prior[time]:
                            wordCity[c]=likelihood[0],
                            postPred[c]=likelihood[1]*prior[time][c]
                            NormFactor=NormFactor+likelihood[1]*prior[time][c]
                           
                        else:
                            wordCity[c]=""
                            postPred[c]=0
                                
                    prediction=self.normalize(postPred,NormFactor)
                    
                    self.fileWrite(row,prediction)
                    #print(float(popDist[prediction[0]])/float(sum(popDist.values())),prediction[1])
                    #if prediction[1]>float(popDist[prediction[0]])/float(sum(popDist.values())):
                    #    print(row[-1],prediction[0],groundTruth)
                    
    def fileWrite(self,data,prediction):
        
        
        output=[]
        ignoreFlag=str(0)
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
    
    def normalize(self,likelihood,norm):
        #temp=0
        for c in likelihood:
            likelihood[c]=likelihood[c]/float(norm)
            #temp=temp+likelihood[c]
        #sortCity = sorted(likelihood.items(), key=operator.itemgetter(1))[::-1]       #sorted Features    
        return(likelihood)
        
         
    
    def maxWords(self,feature,mxW):
        if mxW == 0:
            wordlist=[]
            posterior=1
            for f in feature:
                posterior=posterior*feature[f]
                wordlist.append(f)
            return(wordlist,posterior)
        else:
            posterior=1
            wordlist=[]
            sortFeat = sorted(feature.items(), key=operator.itemgetter(1))       #sorted Features
            sortFeat=sortFeat[::-1]
            for i in range(0,min(len(sortFeat),mxW)):
                posterior=sortFeat[i][1]*posterior
                wordlist.append(sortFeat[i][0])
            return(wordlist,posterior)
                
        
        
        
    def priorCity(self,prediction):
        return(sorted(prediction.items(), key=operator.itemgetter(1))[::-1][0][0])       #sorted Features  

    
        
        
        
        
        
        
        
        
class training(object):  
    def popDist(self,users,data):
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
        print('Data Structure Generation: Complete')
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
                    
        #print(priors)
        return(t,priors)
        
"2017-10-20 23:44:53"

A=NaiveBayes('IA','hashtag',0)#,["2017-10-20"])
#A.crossValidation()


t0 = threading.Thread(target=A.crossValidation,args=(0,1))
t0.daemon =True
t0.start()
t1 = threading.Thread(target=A.crossValidation,args=(1,1))
t1.daemon =True
t1.start()
t2 = threading.Thread(target=A.crossValidation,args=(2,1))
t2.daemon =True
t2.start()
t3= threading.Thread(target=A.crossValidation,args=(3,1))
t3.daemon =True
t3.start()
t4 = threading.Thread(target=A.crossValidation,args=(4,1))
t4.daemon =True
t4.start()
t5 = threading.Thread(target=A.crossValidation,args=(5,1))
t5.daemon =True
t5.start()
t6 = threading.Thread(target=A.crossValidation,args=(6,1))
t6.daemon =True
t6.start()
t7 = threading.Thread(target=A.crossValidation,args=(7,1))
t7.daemon =True
t7.start()
t8 = threading.Thread(target=A.crossValidation,args=(8,1))
t8.daemon =True
t8.start()
t9 = threading.Thread(target=A.crossValidation,args=(9,1))
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