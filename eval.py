
import operator
def Baseline(state,type,W,MX):
    cities={}
    File=open(state+"CityDistsortedProbs").read().split('\n')
    for i in range(0,len(File)):
        row=File[i]
        if len(row)>0:
            row=row.split('|')
            cities[row[0]]=float(row[1])    
    
    #print(cities)
    File=open('tweet'+state+"FormatFull").read().split('|')
    
    index={}
    for i in range(0,len(File)):
        index[i]=File[i]
    priorProbs=[]
    for i in range(6,len(index)):   
        priorProbs.append(str(cities[index[i]]))
        #print(cities[index[i]],index[i])
    
    Write=open('Predicted_'+state+'_W_0_MX_0_baseline.csv','w')
    File=open('Predicted_'+state+'_W_'+str(W)+'_MX_'+str(MX)+'_'+type+'.csv').read().split('\n')
    for j in range(0,len(File)):
        row=File[j].split('|')
        A=len(row)
        row=row[:6]+priorProbs
        B=len(row)
        if A!=B:
            print(A,B)
        Write.write("|".join(row)+'\n')
        
    Write.close()
    


def Eval(state,type,W,MX,sub=True):
    File=open('tweet'+state+"FormatFull").read().split('|')
    
    index={}
    for i in range(0,len(File)):
        index[i]=File[i]
    #print(index)
    
    
    File=open('Gazette'+state+".csv").read().split('\n')
    gazette=[]
    for i in range(0,len(File)):
        if len(File[i])>0:
            gazette.append(File[i])
    
    cities={}
    File=open(state+"CityDistsortedProbs").read().split('\n')
    for i in range(0,len(File)):
        row=File[i]
        if len(row)>0:
            row=row.split('|')
            cities[row[0]]=float(row[1])    
            
    File=open('Predicted_'+state+'_W_'+str(W)+'_MX_'+str(MX)+'_'+type+'.csv').read().split('\n')
    j=0
    Error=[]
    for j in range(0,len(File)):
        if len(File[j])>0:
            row=File[j].split('|')
            
            if row[0]!="1" and row[1] not in gazette:
                label={}
                #print(len(row))
                #print(index)
                #print(row[-2:])
                for i in range(0,len(row)):
                    
                    label[index[i]]=row[i]
                subtract={}
                
                for c in cities:
                    if c in label:
                        if sub==True:
                            subtract[c]=float(label[c])-cities[c]
                        else:
                            subtract[c]=float(label[c])-0
                flag=1
                ranked=sorted(subtract.items(),key=operator.itemgetter(1),reverse=True)
                for i in range(0,len(ranked)):
                    if ranked[i][0]==row[3]:
                        #if ranked[i][1]==ranked[i-1][1]:
                        #    print(row[1])
                        #print(i,ranked[i])
                        while( ranked[i][1]==ranked[i-1][1]):
                            i=i-1
                        Error.append(i)
                        flag=0
                        break
                if flag==1:
                    print(row[1])
    Error.sort()
    return(Error)
#Baseline('IA','hashtag','0','3')        
MX1S=Eval('IA','hashtag','0','0')    
MX3S=Eval('IA','hashtag','0','3')    
MX1=Eval('IA','hashtag','0','0',False)    
MX3=Eval('IA','hashtag','0','3',False)    
base=Eval('IA','baseline','0','0',False)    

Eval=open("Res",'w')
Temp=[]
for i in MX1S:
    Temp.append(str(i))
    
Eval.write(','.join(Temp)+'\n')    

Temp=[]
for i in MX3S:
    Temp.append(str(i))
    
Eval.write(','.join(Temp)+'\n')


Temp=[]
for i in MX1:
    Temp.append(str(i))
    
Eval.write(','.join(Temp)+'\n')

Temp=[]
for i in MX3:
    Temp.append(str(i))
    
Eval.write(','.join(Temp)+'\n')

Temp=[]
for i in base:
    Temp.append(str(i))
    
Eval.write(','.join(Temp)+'\n')