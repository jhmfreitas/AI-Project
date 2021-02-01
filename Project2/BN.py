#87671-Joao Freitas 87693-Pedro Soares Grupo 15
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 15 15:51:49 2018

@author: mlopes
"""

class Node():
    def __init__(self, prob, parents = []):
        self.parents=parents;
        self.prob=prob;
    
    def computeProb(self, evid):
        
        if len(self.parents)==0:
            return [1-self.prob[0],self.prob[0]]
        
        else:
            ev=[]
            for i in range(0,len(self.parents)):
                ev+=[evid[self.parents[i]]]
            
            result=self.prob[ev[0]]
            for i in range(1,len(ev)):
                result=result[ev[i]]
            
            return [1-result,result]
    
class BN():
    def __init__(self, gra, prob):
        self.graph=gra;
        self.probs=prob;
    
    def generateEvids(self, n):
        evids=()
        for i in range(1<<n):
            aux=bin(i)[2:]
            aux='0'*(n-len(aux))+aux
            evids+=(tuple(aux),)
        
        return evids
    
    def computePostProb(self, evid):
        alpha=0
        first=0
        second=0
        unknown=[] #unknown variables
        principal=[]
        general=len(evid)*[1,] 
        
        for i in range(0,len(evid)):
            if(evid[i]==[]):
                unknown+=[i]
            
            elif(evid[i]==-1):
                principal+=[i]
                
            else:
                general[i]=evid[i]
                
        evids=self.generateEvids(len(unknown))
        
        if(len(unknown)!=0):
            for i in range(0,len(evids)):
                copy=general[:]
                
                for j in range(0,len(evids[0])):
                    #create evidence
                    copy[unknown[j]]=int(evids[i][j])
                    
                first+=self.computeJointProb(tuple(copy))
                copy[principal[0]]=0
                second+=self.computeJointProb(tuple(copy))
        else:
            aux=tuple(general)
            first+=self.computeJointProb(aux)
            aux=list(aux)
            aux[principal[0]]=0
            second+=self.computeJointProb(tuple(aux))  

        alpha=1/(first+second)
        
        return alpha*first
        
        
    def computeJointProb(self, evid):
        prob=1
        i=0
        for node in self.probs:
            prob*=node.computeProb(evid)[evid[i]]
            i+=1
        return prob