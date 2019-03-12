'''
Examples of input at the bottom of the file

This script uses the dictionary extracted from https://norvig.com/big.txt and checks the following

The script outputs the following
Word,isDictionary, rank, prob, isGazette,correction

Word: The Word
isDictionary: This =1 if the word is in the dictionary ,0 otherwise
rank: if the word is in the dictionary, return the relative rank of the word
prob: Return the relative frequency of the word, if it is in the dictionary
isGazette: is the word in the Gazette (including corrections), if it is not in the dictionary. 
        This is =1 if the word is in the Gazetteer (but not in the dictionary), 0 otherwise
correction: if the word is in the gazetteer, what is the gazette corrected word within an edit distance =2



Currently the default state is Iowa and the gazetteer being used is the 2012 one.
To change state, just update line 143
To use a more current gazetteer, update line 55 with the new gazetteer's name
'''
file1=open('mwFreq.txt','w')
file2=open('notFoundWords.txt','w')
file3=open('misspellWords.txt','w')

input=open('tempAtempMWS_IA_htsNouns-Freq.txt','r', encoding="utf-8").read().split('\n')
#from nltk.corpus import wordnet as wn
import re
from collections import Counter
import operator
import operator
from wordfreq import word_frequency as wf       #pip install wordfreq


class wordFreq(object):
    def WORDS(self,word):
        if wf(word,'en')>=1.0e-07 :#len(wn.synsets(word))>0:
            return(True)
        else:
            return(False)
    def P(self,word): 
        "Probability of `word`."
        
        return wf(word,'en')
   
    '''def Rank(self,word):    
        "Rank of the word"
        return(self.rank[word])
    '''    
        
        
class GazetteDictionary(object):        
    def __init__(self,state="IA"):
        self.statePath = state+'_Features_20121204.txt'
        self.gazette = self.gazetteGenerator()
        self.WORDS = Counter(self.gazette)

    def gazetteGenerator(self):
        file=open(self.statePath,'r', encoding="utf-8").read().split('\n')
        localGazette=[]
        for i in range(1,len(file)):
            row=file[i].split('|')
            #print(row)
            if len(row)>1:
                currName=row[1].strip()
                if row[-3].find('Unknown')==-1:     #Location not unknown
                    localGazette.append(currName.lower())
                    name=currName.replace(" ","")
                    if name !=currName:
                        localGazette.append(name.lower())
                    name=currName.replace(" ",'-')
                    if name != currName:
                        localGazette.append(name.lower())
                        
                    name=currName.replace(" ","_")
                    if name !=currName:
                        localGazette.append(name.lower())
        
        return(list(set(localGazette)))
                        
        
        
    
        
        
    #def words(self,text): return re.findall(r'\w+', text.lower())
   
    def P(self,word): 
        "Probability of `word`."
        N=sum(self.WORDS.values())
        return self.WORDS[word] / N        
    def correction(self,word): 
        "Most probable spelling correction for word."
        return max(self.candidates(word), key=self.P)

    def candidates(self,word): 
        "Generate possible spelling corrections for word."
        return (self.known([word]) or self.known(self.edits1(word)) or self.known(self.edits2(word)) or [word])

    def known(self,words): 
        "The subset of `words` that appear in the dictionary of WORDS."
        return set(w for w in words if w in self.WORDS)

    def edits1(self,word):
        "All edits that are one edit away from `word`."
        letters    = 'abcdefghijklmnopqrstuvwxyz'
        splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
        deletes    = [L + R[1:]               for L, R in splits if R]
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
        replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
        inserts    = [L + c + R               for L, R in splits for c in letters]
        return set(deletes + transposes + replaces + inserts)

    def edits2(self,word): 
        "All edits that are two edits away from `word`."
        return (e2 for e1 in self.edits1(word) for e2 in self.edits1(e1))


def wordStat(W,G,D):
    #word,isDictionary, rank, prob, isGazette,correction
    isDictionary=0
    rank=-1
    prob=-1
    isGazette=0
    correction=""
    if D.WORDS(W)==True:
        isDictionary=1
        
        
        prob=D.P(W)
        return([W,isDictionary, prob, isGazette,correction])
    
    
    gazetterCorrection=G.correction(W)
    if gazetterCorrection not in G.WORDS:
        return([W,isDictionary, prob, isGazette,correction])
        
    return((W,isDictionary,prob,1,gazetterCorrection))
    
    
freqmxW={}        
gazette=GazetteDictionary()
dictionary=wordFreq()
x=0
mxW=[]
for r in input:
    if len(r) >0:
        row=r.split('|')
        i=row[0]
        
        W=wordStat(i,gazette,dictionary)
        if W[1]==1:
            mxW.append([W[0],W[2]])
            
            freqmxW[row[0]]=float(row[1])
            x=x+float(row[1])
        if W[3]==1:
            file3.write(W[0]+'|'+W[4]+'\n')
        if W[1]==0 and W[3]==0:
            file2.write(W[0]+'\n')
#Examples:

basemxW={}
for m in mxW:
	basemxW[m[0]]=m[1]
	

sortbase=sorted(freqmxW.items(),key=operator.itemgetter(1),reverse=True)	

for s in sortbase:
	file1.write(s[0]+'|'+str(s[1]/float(x))+'|'+str(float(basemxW[s[0]]))+'\n')
'''
print(wordStat('iowacity',gazette,dictionary))
print(wordStat('iowaxity',gazette,dictionary))
print(wordStat('iowacccccccccity',gazette,dictionary))
print(wordStat('apple',gazette,dictionary))
'''
file1.close()
file2.close()
file3.close()
