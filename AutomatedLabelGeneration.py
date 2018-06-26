File=open('Entropy.csv').read().split('\n')
Complete=[]
counts=[]
time=[]
space=[]
st=[]
for i in range(1,len(File)):
    if len(File[i])>0:
        row=[]
        temp=File[i].split(',')
        for j in range(0,len(temp)-1):
            row.append(temp[j])
        Complete.append(row)
        counts.append(int(temp[1]))
        time.append(float(temp[2]))
        space.append(float(temp[3]))
        st.append(float(temp[4]))
            
for i in range(0,len(Complete)):
    Complete[i][1]=float(Complete[i][1])/max(counts)
    Complete[i][2]=float(Complete[i][2])/max(time)
    Complete[i][3]=float(Complete[i][3])/max(space)
    Complete[i][4]=float(Complete[i][4])/max(st)
    Complete[i].append(Complete[i][3]-Complete[i][2])
    
    
    if Complete[i][4]<=0.01906:
        Complete[i].append(4)
    elif Complete[i][5]<0.027158:
        if Complete[i][5]<-0.202161:
            Complete[i].append(2)
        else:
            Complete[i].append(1)
    else:
        if Complete[i][5]>0.11294:
            Complete[i].append(3)
        else:
            Complete[i].append(1)
            
            
F=open('Label.csv','w')
for row in Complete:
    for i in range(0,len(row)):
        row[i]=str(row[i])
    F.write(','.join(row)+'\n')