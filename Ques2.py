import collections
from collections import defaultdict
import sys

def lookup(l, tag):
    if len(l) == 32768 and (not first_seen[(tag,1)]):
        first_seen[(tag,1)] = True
        return [False,1]

    for i in l:
        if i[0]==tag and i[1] ==1:
            #update lru state
            i[2] += 1
            return [True,0]
    
    return [False,2]


def replace(l, tag):
    global l2, l3
    empty = False
    for i in l:
        if i[0] is None:
            empty = True
            i = [tag,1,1]
            break
    
    if not empty:
        invalid = False
        for i in l:
            if i[0] != None and i[2] == 0:
                invalid = True
                i = [tag,1,1]
                break
        if not invalid:
            maxtime = 0
            cacheline = 0
            for i in l:
                if i[2] > maxtime:
                    maxtime = i[2]
                    cacheline = l.index(i)
            if len(l) == 32768:
                for j in l2:
                    if j[0] == tag:
                        j[2] = 0
            l[cacheline] = [tag, 1, 1]
            



print()
fname=[["gromacs.log_l1misstrace",1],["h264ref.log_l1misstrace",1],["hmmer.log_l1misstrace",1],["sphinx3.log_l1misstrace",2],["bzip2.log_l1misstrace",2],["gcc.log_l1misstrace",2]]
fname.sort()

for name in fname: 
    first_seen=defaultdict(lambda: False)

    l2 = [[None, 0, 0] for i in range(8192)]
    l3 = [[None, 0 ,0] for i in range(32768)]

    l2_capacity_misses = 0
    l2_compulsory_misses = 0
    l3_capacity_misses = 0
    l3_compulsory_misses = 0
    l2_misses = 0
    l3_misses = 0

    for num in range(name[1]): 
        f=open(name[0]+"_"+str(num)+".txt",'r')
        addresses=[int(z[:-2]) for z in f] 
        count = 0
        for x in addresses:
            
            x = bin(x)[2:]
            x = ((64-len(x))*'0') + x

            tag = int(x[:-6],2)
    
            hit2 = lookup(l2, tag)

            if not hit2[0]:
                l2_misses += 1
                hit3 = lookup(l3, tag)

            if not hit3[0]:
                if hit3[1]==1:
                    l3_compulsory_misses += 1
                l3_misses += 1
                replace(l3, tag)
                replace(l2, tag)

    print("simulation done for file "+name[0]+" and following are required values : ")
    print("Total l2 misses = ",l2_misses)
    print("Total l3 misses = ",l3_misses)


    print("L3 cold misses = ",l3_compulsory_misses)
    print("L3 conflict misses = ",l3_misses-l3_compulsory_misses)
    print()
    print("============================================================")
    print() 