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
      #print("k="+str(k))
      for i in range(k):
          if (l[s][i])[0]==t: 
                (l[s][i])[2]=0
                break
      for j in range(k):
            #print("j="+str(j))
            if (l[s][j])[0]!=None and (l[s][j])[1] ==1:
                 (l[s][j])[2] = (l[s][j])[2] + 1

def replace(l,s,t,k):      
      empty=False
      for i in range(k):
      	  if (l[s][i])[0]==None: # empty line
                #print("empty line")
                empty=True
                (l[s][i])[0]=t 
                (l[s][i])[1]=1
                (l[s][i])[2]=0  
                lru_state(l,s,t,k)
                break 
      
      if not empty:
      	  # find an invalid line
          invalid=False
          for i in range(k):
              if (l[s][i])[1]==0:
                   #print("Invalid line")
                   invalid=True
                   (l[s][i])[0]=t 
                   (l[s][i])[1]=1
                   (l[s][i])[2]=0  
                   lru_state(l,s,t,k)
                   break 
          if not invalid:
              #print("LRU line")
              maxtime=0
              lineno=0  
              for i in range(k):
              	  if (l[s][i])[2] >maxtime:
                     maxtime=(l[s][i])[2]
                     lineno=i
    
              (l[s][lineno])[0]=t 
              (l[s][lineno])[1]=1 
              (l[s][lineno])[2]=0
              lru_state(l,s,t,k) 
              
               
def invalidate(l,b):
      t=int(b[:48],2)
      s=int(b[48:],2)
      for i in range(8):
      	  if (l[s][i])[0]==t:        
              (l[s][i])[1]=0


print()
fname=[["gromacs.log_l1misstrace",1],["h264ref.log_l1misstrace",1],["hmmer.log_l1misstrace",1],["sphinx3.log_l1misstrace",2],["bzip2.log_l1misstrace",2],["gcc.log_l1misstrace",2]]
fname.sort()

for name in fname: 
 
 first_seen=defaultdict(lambda: False)

 l2=[[[None,0,0] for i in range(8)] for j in range(1024)]
 l3=[[[None,0,0] for i in range(16)] for j in range(2048)]

 l2_misses=0
 l3_misses=0 
 l2_hits=0
 l3_hits=0
 cold=0
 conflict=0

 
 for num in range(name[1]): 
  f=open(name[0]+"_"+str(num)+".txt",'r')
  addresses=[int(z[:-2]) for z in f] 
  for x in addresses:

       x=(bin(x))[2:] 
       x=((64-len(x))*'0') + x 

       s2 = int(x[48:-6],2)
       t2 = int(x[:48],2)
     
       
       s3=int(x[47:-6],2)
       t3=int(x[:47],2)
     

       hit2 = lookup(l2,s2,t2,8) 

       if hit2[0]: 
           l2_hits+=1
           lru_state(l2,s2,t2,8)
       else:
       	   l2_misses+=1
           hit3 = lookup(l3,s3,t3,16)  
           #print(hit3[0])
           if hit3[0]:
               l3_hits+=1
               lru_state(l3,s3,t3,16)
               replace(l2,s2,t2,8) 
           else: # bring from memory
               if hit3[1]==1:
                   cold+=1
               else:
                  conflict+=1
               l3_misses+=1
               replace(l3,s3,t3,16)
               replace(l2,s2,t2,8)  
                       
    
 print("simulation done for file "+name[0]+" and following are required values : ")
 print("Total l2 misses = ",l2_misses)
 print("Total l2 hits = ",l2_hits)
 print("Total l3 misses = ",l3_misses)
 print("Total l3 hits = ",l3_hits)

 print("L3 cold misses = ",cold)
 print("L3 conflict misses = ",conflict)
 print()
 print("============================================================")
 print() 
