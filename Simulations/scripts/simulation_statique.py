# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 16:00:43 2026

@author: basti
"""

from scipy.stats import truncnorm
from scipy.stats import gamma
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


##Force de la politique
def phi(n, gamma):
    return gamma * np.log(1 + n)

##Signal de réactance
def reactance_signal(n, T):
    return (n/T)**1.5

###Facteurs fixes
c = 1
Gamma = 0.2
T = 0.9

###Motivation et réactance

mean = 1
std = 0.3

lower = 0
upper = 2

a = (lower - mean) / std
b = (upper - mean) / std

Vi = truncnorm.rvs(a, b, loc=mean, scale=std)

theta_i = gamma.rvs(a=5, scale=1)

utilite = Vi-(c- phi(1, Gamma)) - theta_i * reactance_signal(1, T)

##Fonction d'utilité
def utility(Vi, theta_i, n, c, gamma, T):

    material_effect = phi(n, gamma)

    psychological_cost = theta_i * (n/T)**1.5

    return Vi - c + material_effect - psychological_cost
##Adoption
def adopt(Vi, theta_i, n, c, gamma, T):

    threshold = c - phi(n, gamma) + theta_i * (n/T)**1.5

    return Vi >= threshold

###Test sur 1000 agents
liste_agent = []
for i in range(1000):
    Vi = truncnorm.rvs(a, b, loc=mean, scale=std)
    theta_i = gamma.rvs(a=1, scale=0.3)
    
    liste_agent.append((i, Vi, theta_i))
    
    i+=1

#Pour notre population, on va tester toutes les valeurs de n pour chercher le suil optimal
#Il nous l'utilité de chaque agent pour connaitre son adoption et 
#à chaque simulation de n, on enregistre simplement le taux d'adoption
liste_util = []
liste_part_adopt = []

for val in range(100):
    
    nb_adopt = 0
    
    c = 1
    gamma_phi = 1
    T = 0.9
    
    # Boucle sur tous les agents pour la valeur 'val' en cours
    for i, Vi, theta_i in liste_agent:
        utilite = utility(Vi, theta_i, val, c, gamma_phi, T)
        liste_util.append((val, i, utilite))  # Retrait de la virgule inutile
        
        adoption = adopt(Vi, theta_i, val, c, gamma_phi, T)
        
        if adoption:
            nb_adopt += 1

    part = nb_adopt / len(liste_agent)
    liste_part_adopt.append((val, part))
    
## graphique
val_n = [stat[0] for stat in liste_part_adopt]
val_adopt = [stat[1] for stat in liste_part_adopt]

sns.lineplot(x = val_n, y = val_adopt, color="green")
# Personnalisation
plt.title("Taux d'adoptant avec une variation de n")
plt.xlabel("n")
plt.ylabel("P(n)")
plt.grid(True)

# Affichage
plt.show()


##heatmap
# 1. On initialise un dictionnaire vide pour stocker les colonnes
dictionnaire_heat = {}

# Boucle principale (lignes ou colonnes)
for val in np.arange(0, 10, 0.1):

    # Pour chaque 'val', on va stocker les résultats de tous les 't'
    liste_pour_cette_val = []

    for t in np.arange(0,50,0.5):

        nb_adopt = 0

        for i, Vi, theta_i in liste_agent:
            # OPTIMISATION : Remplacement du paramètre fixe T par la variable de boucle t
            # utilite = utility(Vi, theta_i, val, c, Gamma, t) # Si utile plus tard
            
            # Utilisation de l'astuce : True vaut 1, False vaut 0
            nb_adopt += adopt(Vi, theta_i, val + 1, c, Gamma, t + 1)

        part = nb_adopt / len(liste_agent)
        
        # On ajoute juste la valeur finale de 'part' dans l'ordre chronologique des 't'
        liste_pour_cette_val.append(part)

    # On associe la liste de résultats à la colonne 'val' correspondante
    dictionnaire_heat[val] = liste_pour_cette_val

# 2. Création du DataFrame en un seul bloc
# Les index (lignes) seront automatiquement de 0 à 499 (représentant 't')
# Les colonnes seront de 0 à 499 (représentant 'val')
data_heat = pd.DataFrame(dictionnaire_heat)

# 3. Affichage de la Heatmap
plt.figure(figsize=(12, 10))
sns.heatmap(data_heat, cmap="viridis", xticklabels=50, yticklabels=50)

plt.title("Heatmap du taux d'adoption")
plt.xlabel("Valeur de n (variable val)")
plt.ylabel("Valeur de T (variable t)")
plt.show()
    
        
#Test sur gamma
liste_util = []
liste_part_adopt = []
gamma_values = [0.05, 0.1, 0.25, 0.5, 1]

for valeur in gamma_values :

    nb_adopt = 0
    
    c = 1
    T = 1
    
    liste_agent = []
    for i in range(1000):
        Vi = truncnorm.rvs(a, b, loc=mean, scale=std)
        theta_i = gamma.rvs(a=1, scale=0.05)
        
        liste_agent.append((i, Vi, theta_i))
        
        i+=1         
        
    for val in np.arange(0, 10, 0.1):
        nb_adopt = 0
        # Boucle sur tous les agents pour la valeur 'val' en cours
        for i, Vi, theta_i in liste_agent:
            utilite = utility(Vi, theta_i, val, c, valeur, T)
            liste_util.append((val, i, utilite))  # Retrait de la virgule inutile
            
            adoption = adopt(Vi, theta_i, val, c, valeur, T)
            
            if adoption:
                nb_adopt += 1
        
        part = nb_adopt / len(liste_agent)
        liste_part_adopt.append((valeur, val, part))
        
## graphique
val_g = [stat[0] for stat in liste_part_adopt]
val_n = [stat[1] for stat in liste_part_adopt]
val_adopt = [stat[2] for stat in liste_part_adopt]

sns.lineplot(x = val_n, y = val_adopt, hue=val_g)
# Personnalisation
plt.title("Taux d'adoptant avec une variation de gamma")
plt.xlabel("n")
plt.ylabel("P(n)")
plt.grid(True)

# Affichage
plt.show()


#Test sur T
liste_util = []
liste_part_adopt = []
t_values = [0.1,0.2,0.3,0.5,0.8,1]

for valeur in t_values :

    nb_adopt = 0
    
    c = 1
    T = valeur
    gamma_phi = 0.2 
    
    liste_agent = []
    for i in range(10000):
        Vi = truncnorm.rvs(a, b, loc=mean, scale=std)
        theta_i = gamma.rvs(a=1, scale=0.3)
        
        liste_agent.append((i, Vi, theta_i))
        
        i+=1         
        
    for val in range(100):
    
        nb_adopt = 0   # <-- ici
    
        for i, Vi, theta_i in liste_agent:
    
            utilite = utility(Vi, theta_i, val, c, gamma_phi, T)
    
            liste_util.append((val, i, utilite))
    
            adoption = adopt(Vi, theta_i, val, c, gamma_phi, T)
    
            if adoption:
                nb_adopt += 1
    
        part = nb_adopt / len(liste_agent)
    
        liste_part_adopt.append((T, val, part))
        
## graphique
val_t = [stat[0] for stat in liste_part_adopt]
val_n = [stat[1] for stat in liste_part_adopt]
val_adopt = [stat[2] for stat in liste_part_adopt]

sns.lineplot(x = val_n, y = val_adopt, hue=val_t)
# Personnalisation
plt.title("Taux d'adoptant avec une variation de T")
plt.xlabel("n")
plt.ylabel("P(n)")
plt.grid(True)

# Affichage
plt.show()

##ETUDE DE PHI ET DU SIGNAL DE REACTANCE
import numpy as np
import matplotlib.pyplot as plt

# Paramètres
gamma_phi = 1
T = 1

# moyenne de ta loi Gamma actuelle
# adapte si tu changes la distribution
theta_i = gamma.rvs(a=1, scale=0.05)

# Valeurs de n
n_values = np.linspace(0,100,500)

# Gain matériel
material_gain = gamma_phi * np.log(1+n_values)

# Coût psychologique moyen
reactance_cost = theta_i * (n_values/T)**1.5

# Graphique
plt.figure(figsize=(8,5))

plt.plot(n_values, material_gain, label="Gain matériel φ(n)")
plt.plot(n_values, reactance_cost, label="Coût de réactance moyen")

plt.xlabel("Intensité du nudge n")
plt.ylabel("Valeur dans l'utilité")
plt.title("Comparaison gain matériel vs coût psychologique")
plt.grid(True)
plt.legend()

plt.show()