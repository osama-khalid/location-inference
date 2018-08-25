
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
    
    Write=open('Predicted_'+state+'_W_'+str(W)+'_MX_'+str(99)+'_'+type+'.csv','w')
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
    print(state,type,W,MX)
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
    d=0
    ranks={}
    for j in range(0,len(File)):
        if j%int((len(File)/20))==0:
            print(j)
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
                        if i not in ranks:
                            ranks[i]=[]
                        ranks[i].append(row[3])
                        flag=0
                        break
                if flag==1:
                    d=d+1
    
    return(ranks)

    
def rankedErr(ranks,i=1):
    Temp=[[]]*10
    Temp[0]=list(set(ranks[0]))
    for r in range(1,min(i,len(ranks))):
    
        Temp[r]=Temp[r-1]+list(set(ranks[r]))
        Temp[r]=list(set(Temp[r]))
    return(Temp)

def helper(st,type,w,m,i):    
    ranks=Eval(st,type,w,m,False)    
    MX1=rankedErr(ranks,i)
    file=open("Rank_"+st+"_"+type+"_"+w+"_"+m+"_c_"+str(i),'w')
    for j in range(0,len(MX1)):
        #print(str(j)+','+str(len(MX1[j]))+"\n")
        file.write(str(j)+','+str(len(set(MX1[j])))+"\n")
    file.close()
    

ranks=helper('IA','hashtag','0','1',10)    
ranks=helper('IA','hashtag','0','0',10)    
ranks=helper('IA','hashtag','1','0',10)    
ranks=helper('IA','hashtag','1','1',10)    
ranks=helper('IA','hashtag','3','0',10)    
ranks=helper('IA','hashtag','3','1',10)    
ranks=helper('IA','hashtag','1','1',10)    

ranks=helper('IA','noun','0','1',10)    
ranks=helper('IA','noun','0','0',10)    
ranks=helper('IA','noun','1','0',10)    
ranks=helper('IA','noun','1','1',10)    
ranks=helper('IA','noun','3','0',10)    
ranks=helper('IA','noun','3','1',10)    
ranks=helper('IA','noun','1','1',10)    

ranks=helper('IA','all','0','1',10)    
ranks=helper('IA','all','0','0',10)    
ranks=helper('IA','all','1','0',10)    
ranks=helper('IA','all','1','1',10)    
ranks=helper('IA','all','3','0',10)    
ranks=helper('IA','all','3','1',10)    
ranks=helper('IA','all','1','1',10)    



#ranks=Eval(st,type,w,m,False)    
#MX1=rankedErr(ranks,i)