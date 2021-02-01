#87671-Joao Freitas 87693-Pedro Soares Grupo 15
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 20:31:54 2017

@author: mlopes
"""
import numpy as np
import random

from tempfile import TemporaryFile
outfile = TemporaryFile()
	
class finiteMDP:

    def __init__(self, nS, nA, gamma, P=[], R=[], absorv=[]):
        self.nS = nS #numero de states
        self.nA = nA #numero de acoes
        self.gamma = gamma #gamma - discount factor
        self.Q = np.zeros((self.nS,self.nA)) #valores de Q para todas as trajetorias
        self.P = P
        self.R = R
        self.absorv = absorv
        # completar se necessario
        
            
    def runPolicy(self, n, x0,  poltype = 'greedy', polpar=[]):
        #nao alterar
        traj = np.zeros((n,4)) #vetor para valores de trajetoria
        x = x0
        J = 0

        for ii in range(0,n):
            a = self.policy(x,poltype,polpar) #acao
            r = self.R[x,a] #reward
            y = np.nonzero(np.random.multinomial( 1, self.P[x,a,:]))[0][0] #estado de chegada
            traj[ii,:] = np.array([x, a, y, r]) #calcula trajetoria para cada SARS'
            J = J + r * self.gamma**ii  #funcao a maximizar (funcao J)
            if self.absorv[x]:
                y = x0
            x = y #avanca para estado de chegada x->y
        
        return J,traj


    def VI(self):
        #nao alterar
        nQ = np.zeros((self.nS,self.nA))
        while True:
            self.V = np.max(self.Q,axis=1) 
            for a in range(0,self.nA):
                nQ[:,a] = self.R[:,a] + self.gamma * np.dot(self.P[:,a,:],self.V)
            err = np.linalg.norm(self.Q-nQ)
            self.Q = np.copy(nQ)
            if err<1e-7:
                break
            
        #update policy
        self.V = np.max(self.Q,axis=1) 
        #correct for 2 equal actions
        self.Pol = np.argmax(self.Q, axis=1)
                    
        return self.Q,  self.Q2pol(self.Q)

            
    def traces2Q(self, trace): #calcula valores de Q para todas as trajetorias
        # implementar esta funcao
        self.Q = np.zeros((self.nS,self.nA))
        temporaryQ = np.zeros((self.nS, self.nA))
        
        alpha=0.1
        
        while True:
            for elem in trace:
                s=int(elem[0])
                a=int(elem[1])
                r=elem[3]
                s_next=int(elem[2])
                
                temporaryQ[s,a] += alpha*(r+self.gamma*max(temporaryQ[s_next,:]) - temporaryQ[s,a])
            
            dif = np.linalg.norm(self.Q - temporaryQ)
            self.Q = np.copy(temporaryQ)
        
            if dif < 1e-2:
                break     
            
        return self.Q
    
    def policy(self, x, poltype = 'exploration', par = []):
        # implementar esta funcao
        
        if poltype == 'exploitation':
            #usa o polpar e verifica qual a melhor acao para o seu estado
            a=np.argmax(par[x])#retorna index do maior valor para aquele estado(retorna s' = proximo estado)
            
            
        elif poltype == 'exploration':
            #randint(self.nA - 1)
            a=np.random.randint(0,self.nA) #explora de forma aleatoria para explorar melhor o ambiente

                
        return a
    
    def Q2pol(self, Q, eta=5):
        # implementar esta funcao
        return np.exp(eta*Q)/np.dot(np.exp(eta*Q),np.array([[1,1],[1,1]]))