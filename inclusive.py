
import collections
from collections import defaultdict

def lookup(l,s,t,k):
       if len(l)==2048 and (not first_seen[(s,k)]):
           first_seen[(s,k)]=True
           return [False,1]

       for i in range(k):
           if (l[s][i])[0]==t and (l[s][i])[1]==1:
           	    return [True,0]
       
       return [False,2] 

def lru_state(l,s,t,k):
      
      for i in range(k):
          if (l[s][i])[0]==t: 
                (l[s][i])[2]=0
                break

      for i in range(k):          
           if (l[s][i])[0]!=-1 and (l[s][i])[1]==1:
           	    (l[s][i])[2]=(l[s][i])[2]+1
      return l

def replace2(l,s,t):
     empty=False                  
     for i in range(8):
          if (l[s][i])[0]==-1:
              empty=True
              (l[s][i])[0]=t  
              (l[s][i])[1]=1 
              (l[s][i])[2]=0
              return l
             
     if not empty:
         invalid=False
         for i in range(8):
             if (l[s][i])[1]==0:
                invalid=True
                (l[s][i])[0]=t  
                (l[s][i])[1]=1 
                (l[s][i])[2]=0
                return l
                

         if not invalid:
             m=0
             line=0
             for i in range(8):
                  if (l[s][i])[2]>m:
                     m = (l[s][i])[2]
                     line=i
             (l[s][line])[0]=t           
             (l[s][line])[1]=1         
             (l[s][line])[2]=0
             return l

def replace3(l,s,t):
     empty=False                  
     for i in range(16):
          if (l[s][i])[0]==-1:
              empty=True
              (l[s][i])[0]=t  
              (l[s][i])[1]=1 
              (l[s][i])[2]=0
              return [l,-1,False]

     if not empty:
         invalid=False
         for i in range(16):
             if (l[s][i])[1]==0:
                invalid=True
                (l[s][i])[0]=t  
                (l[s][i])[1]=1 
                (l[s][i])[2]=0
                return [l,-1,False]

         if not invalid:
             m=0
             line=0
             for i in range(8):
                  if (l[s][i])[2]>m:
                     m = (l[s][i])[2]
                     line=i
             tag = (l[s][line])[0]
             tag = (bin(tag))[2:]
             sett= (bin(s))[2:]
                 
             tag= ((47-len(tag))*'0')+tag
             sett=((11-len(sett))*'0')+sett
             
             (l[s][line])[0]=t           
             (l[s][line])[1]=1         
             (l[s][line])[2]=0 
             
             return [l,tag+sett,True] 



def invalidate(l,b):
      #print("HERE")
      #print("b=",b)
      t=int(b[:48],2)
      s=int(b[48:],2)
      for i in range(8):
      	  if (l[s][i])[0]==t:        
              (l[s][i])[1]=0 
      return l



fname=[["gromacs.log_l1misstrace",1],["h264ref.log_l1misstrace",1],["hmmer.log_l1misstrace",1],["sphinx3.log_l1misstrace",2],["bzip2.log_l1misstrace",2],["gcc.log_l1misstrace",2]]
fname.sort()

for name in fname: 
#for name in [["hmmer.log_l1misstrace",1]]:

    first_seen=defaultdict(lambda: False)

    l2=[[[-1,0,0] for i in range(8)] for j in range(1024)]
    l3=[[[-1,0,0] for i in range(16)] for j in range(2048)]
    
    l2_misses=0
    l3_misses=0
    l2_hits=0
    l3_hits=0 
    cold=0
    conflict=0
    capacity=0
    count=0
    for num in range(name[1]): 
         f=open(name[0]+"_"+str(num)+".txt",'r')
         addresses=[int(z[:-2]) for z in f] 	
         for x in addresses:
               x=(bin(x))[2:] 
               x =((64-len(x))*'0') + x    
               
               s2 = int(x[48:-6],2)
               t2 = int(x[:48],2)
     
               s3=int(x[47:-6],2)
               t3=int(x[:47],2)

               hit2=lookup(l2,s2,t2,8)
               
               if hit2[0]:
               	    l2_hits+=1
               	    l2=lru_state(l2,s2,t2,8)
                    
               else:
                   l2_misses+=1 
                   hit3=lookup(l3,s3,t3,16)

                   if hit3[0]: 
                      l3_hits+=1
                      l3=lru_state(l3,s3,t3,16)
                      l2=replace2(l2,s2,t2)
                      l2=lru_state(l2,s2,t2,8)
                   else:   
                       l3_misses+=1
                       q=replace3(l3,s3,t3)  
                       if q[1]!=-1:
                       	  #print("q= ",q[1])
                       	  l2=invalidate(l2,q[1])
                       	  count+=1
                       if q[2]:
                          capacity+=1	  
                       if hit3[1]==1:
                          cold+=1
                       else:
                          conflict+=1  

                       l3=q[0]	  
                       l3=lru_state(l3,s3,t3,16)    
                       
                       l2=replace2(l2,s2,t2)
                       l2=lru_state(l2,s2,t2,8) 




                     
    print()
    print("simulation done for file "+name[0]+" and following are required values : ")
    
    print("Total l2 misses = ",l2_misses)
    print("Total l2 hits = ",l2_hits)
    print("Total l3 misses = ",l3_misses)
    print("Total l3 hits = ",l3_hits)
    print("L3 cold misses = ",cold)
    print("L3 conflict misses = ",conflict)
    print("L3 capacity misses = ",capacity)
    print("Total misses = ",(cold+conflict+capacity))
    print("invalidate count = ",count)
    
    print("================================================================")






















