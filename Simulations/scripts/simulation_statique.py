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


##Force de la politique
def phi(n, gamma):
    return gamma * np.log(1 + n)

##Signal de réactance
def reactance_signal(n, T):
    return np.tanh(n / T)

###Facteurs fixes
c = 1
Gamma = 0.5
T = 1

###Motivation et réactance

mean = 1
std = 0.3

lower = 0
upper = 2

a = (lower - mean) / std
b = (upper - mean) / std

Vi = truncnorm.rvs(a, b, loc=mean, scale=std)

theta_i = gamma.rvs(a=2, scale=0.25)

utilite = Vi-(c- phi(1, Gamma)) - theta_i * reactance_signal(1, T)

##Fonction d'utilité
def utility(Vi, theta_i, n, c, gamma, T):

    material_effect = phi(n, gamma)

    psychological_cost = theta_i * np.tanh(n / T)

    return Vi - c + material_effect - psychological_cost
##Adoption
def adopt(Vi, theta_i, n, c, gamma, T):

    threshold = c - phi(n, gamma) + theta_i * np.tanh(n / T)

    return Vi >= threshold

###Test sur 1000 agents
liste_agent = []
for i in range(1000):
    Vi = truncnorm.rvs(a, b, loc=mean, scale=std)
    theta_i = gamma.rvs(a=2, scale=0.25)
    
    U = utility(Vi, theta_i, 1, c, Gamma, T)
    adoption = adopt(Vi, theta_i, 1, c, Gamma, T)
    
    liste_agent.append((i, U, adoption))
    
    i+=1

###Graphiques
# zip(*...) va créer un groupe pour les 'i', un pour les 'U', et un pour les booléens
axes_x, axes_y, axes_z = zip(*liste_agent)

# Génération du graphique
plt.plot(axes_z, axes_x, marker='o', linestyle='-', color='b')

# Personnalisation
plt.title("Évolution de U en fonction de l'index i")
plt.xlabel("Index (i)")
plt.ylabel("Valeur de U")
plt.grid(True)

# Affichage
plt.show()


# On extrait uniquement les valeurs de U (la deuxième colonne)
valeurs_U = [stat[1] for stat in liste_agent]

# Création du graphique de densité
sns.kdeplot(valeurs_U, fill=True, color="green")

# Personnalisation
plt.title("Graphique de densité des valeurs de U")
plt.xlabel("Valeurs de U")
plt.ylabel("Densité de probabilité")
plt.grid(True)

# Affichage
plt.show()
    

###Histogramme
from collections import Counter

# On sépare vos données comme vous l'avez fait
axes_x, axes_y, axes_z = zip(*liste_agent)

# 1. On compte automatiquement le nombre de True et de False
comptage = Counter(axes_z)

# 2. On sépare les étiquettes (True/False) et leurs volumes (les valeurs)
categories = list(comptage.keys())  # Contient [False, True] (ou inversement)
volumes = list(comptage.values())  # Contient le nombre de chaque

# Génération du graphique en barres (plt.bar au lieu de plt.plot)
# On peut même donner des couleurs différentes : rouge pour False, vert pour True
couleurs = ['green' if cat else 'red' for cat in categories]
plt.bar(categories, volumes, color=couleurs, width=0.4)

# Personnalisation
plt.title("Volume des états (True / False)")
plt.xlabel("État (axes_z)")
plt.ylabel("Volume (Nombre d'agents)")

# On force l'affichage de "True" et "False" proprement sur l'axe X
plt.xticks(categories, [str(cat) for cat in categories])

plt.grid(axis='y', linestyle='--', alpha=0.7)  # Grille uniquement horizontale

# Affichage
plt.show()

##Boucle en faisant varier n sur un agent
liste_n=[]

for n in range(200):
    Vi = truncnorm.rvs(a, b, loc=mean, scale=std)
    theta_i = gamma.rvs(a=2, scale=0.25)
    
    U = utility(Vi, theta_i, n, c, Gamma, T)
    adoption = adopt(Vi, theta_i, n, c, Gamma, T)
    
    liste_n.append((n, U, adoption))
    
    n+=1

valeurs_U = [stat[1] for stat in liste_n]

# Création du graphique de densité
sns.kdeplot(valeurs_U, fill=True, color="green")

# Personnalisation
plt.title("Graphique de densité des valeurs de U")
plt.xlabel("Valeurs de U")
plt.ylabel("Densité de probabilité")
plt.grid(True)

# Affichage
plt.show()

# zip(*...) va créer un groupe pour les 'i', un pour les 'U', et un pour les booléens
axes_x, axes_y, axes_z = zip(*liste_n)

# Génération du graphique
plt.plot(axes_x, axes_y, marker='o', linestyle='-', color='b')

# Personnalisation
plt.title("Évolution de U en fonction de l'index i")
plt.xlabel("Index (i)")
plt.ylabel("Valeur de U")
plt.grid(True)

# Affichage
plt.show()