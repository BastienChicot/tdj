# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 13:49:30 2022

@author: bchicot
"""
from itertools import combinations, permutations, islice
import random
import numpy as np
import pandas as pd

##DILEMME DU PRISONNIER

class jeu():
    def __init__(self,nb_joueur,liste_choix):
        self.matrice = pd.DataFrame(index=[liste_choix][0],columns=[liste_choix])
        
        self.nb_joueur = nb_joueur
        
        self.liste_gain = []
        
        self.liste_choix = liste_choix
        
        self.nb_choix = int(len(liste_choix))        
        
        self.optimum  = []
        
        self.df_nash = []
        # for col in self.matrice.columns:
        #     try :
        #         self.a = self.matrice.loc[self.matrice[col] == self.optimum_pareto] 
        #         self.a = self.a.index[0]
        #     except:
        #         pass

    def matrice_gain(self,liste_outcome):
        longueur = int(len(liste_outcome))
        for i in range(0,len(liste_outcome)):
            for i in range(0,self.nb_choix):
                gain = [liste_outcome[i],liste_outcome[i]]
                self.liste_gain.append(gain)

            rest = liste_outcome[self.nb_choix:longueur]
            output=[rest[j:j + self.nb_joueur] for j in range(0, len(rest), self.nb_joueur)]
            for elt in output:
                combi = list(set(permutations(elt,self.nb_joueur)))
                for elt in combi:
                    self.liste_gain.append(list(elt))
                
            self.liste_gain = self.liste_gain[0:len(liste_outcome)]

            return(self.liste_gain)
        
    def show_matrice(self):
        for i in range(len(self.liste_gain)):
            for j in range(len(self.matrice.columns)):
                print(i,j,self.liste_gain[i])
                if i == j and i < len(self.liste_choix):
                    self.matrice.iloc[j][self.matrice.columns[j]] = self.liste_gain[i]
                elif  len(self.liste_gain)-1 > i >= len(self.liste_choix) and i != j:
                    for k in range(len(self.matrice.index)):
                        if k != j :
                            self.matrice.iloc[k][self.matrice.columns[j]] = self.liste_gain[i]
                            self.matrice.iloc[j][self.matrice.columns[k]] = self.liste_gain[i+1]

                    
        return(self.matrice)
        
    def pareto(self):
        if self.matrice.isnull().any().any():
            liste_opti = []
            for i in range(len(self.liste_gain)):
                somme = sum(self.liste_gain[i])
                liste_opti.append(somme)
                
            optimum_idx = [i for i, j in enumerate(liste_opti) if j == max(liste_opti)]
            
            for k in range(len(optimum_idx)) :
                temp = [self.liste_gain[optimum_idx[k]],liste_opti[optimum_idx[k]]]
                self.optimum.append(temp)
     
            return(self.optimum)
        
        else :
            liste_opti = []
            for elt in self.matrice.columns:
                for i in (self.matrice[elt].values):
            
                    liste_opti.append([sum(i), i, elt])
                
            self.optimum  = max(liste_opti)
            return(max(liste_opti))
                
          
    def nash(self):
        if self.matrice.isnull().any().any(): 
            self.matrice = self.show_matrice()
            nash_table = self.matrice.copy()
            for i in range(len(nash_table.index)):
                for j in nash_table.columns:
                    nash_table[j][i] = nash_table[j][i][0]
            for j in nash_table.columns:
                nash_table[j] = nash_table[j].astype(int)
                
            self.df_nash = pd.DataFrame(nash_table.idxmax(axis=1)).reset_index()
            self.eqs = self.df_nash.groupby(0).nunique()
        else:
            nash_table = self.matrice.copy()
            for i in range(len(nash_table.index)):
                for j in nash_table.columns:
                    nash_table[j][i] = nash_table[j][i][0]
            for j in nash_table.columns:
                nash_table[j] = nash_table[j].astype(int)
                
            self.df_nash = pd.DataFrame(nash_table.idxmax(axis=1)).reset_index()
            self.eqs = self.df_nash.groupby(0).nunique()
        
        if len(self.eqs) == 1:
            message = "Un seul équilibre possible : "
            
        else :
            message = "Plusieurs équilibres possibles : "
        
        return(self.df_nash,message,self.eqs)

            
test = jeu(2,["denoncer","rien dire"])                

liste_choix = [-3,-1,0,-10]

a = test.matrice_gain(liste_choix)

test.nash()
b = test.show_matrice()
test.pareto()
test.matrice
test_df = b.copy()

for i in range(len(test_df.index)):
    for j in test_df.columns:
        test_df[j][i] = test_df[j][i][0]#.astype(str).astype(int)
        print(type(test_df[j][i]))
    x = max(test_df.iloc[i])

for j in test_df.columns:
    test_df[j] = test_df[j].astype(int)
liste_nash = pd.DataFrame(test_df.idxmax(axis=1)).reset_index()
eq = liste_nash.groupby(0).nunique()

len(eq)