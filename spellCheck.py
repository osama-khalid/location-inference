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


import re
from collections import Counter
import operator



class norvigDictionary(object):
    
    def __init__(self):
        self.WORDS = Counter(self.words(open('big.txt').read()))

        self.SORT=sorted(self.WORDS.items(),key=operator.itemgetter(1),reverse=True)

        self.rank={}
        for i in range(0,len(self.SORT)):
            self.rank[self.SORT[i][0]]=i+1

    def words(self,text): return re.findall(r'\w+', text.lower())
    
    def P(self,word): 
        "Probability of `word`."
        N=sum(self.WORDS.values())
        return self.WORDS[word] / N
   
    def Rank(self,word):    
        "Rank of the word"
        return(self.rank[word])
        
class GazetteDictionary(object):        
    def __init__(self,state="IA"):
        self.statePath = state+'_Features_20121204.txt'
        self.gazette = self.gazetteGenerator()
        self.WORDS = Counter(self.gazette)

    def gazetteGenerator(self):
        file=open(self.statePath,'r').read().split('\n')
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
    if W in D.WORDS:
        isDictionary=1
        
        rank=D.Rank(W)
        prob=D.P(W)
        return([W,isDictionary, rank, prob, isGazette,correction])
    
    
    gazetterCorrection=G.correction(W)
    if gazetterCorrection not in G.WORDS:
        return([W,isDictionary, rank, prob, isGazette,correction])
        
    return((W,isDictionary,rank,prob,1,gazetterCorrection))
    
    
        
gazette=GazetteDictionary()
dictionary=norvigDictionary()


#Examples:
print(wordStat('iowacity',gazette,dictionary))
print(wordStat('iowaxity',gazette,dictionary))
print(wordStat('iowacccccccccity',gazette,dictionary))
print(wordStat('apple',gazette,dictionary))
