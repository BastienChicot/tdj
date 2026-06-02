import numpy as np
import matplotlib.pyplot as plt

# =========================================================
# 1. Fonctions du modèle
# =========================================================

def phi(n, gamma):
    return gamma * np.log(1 + n)

def reactance_term(n, theta, T):
    return theta * np.tanh(n / T)

def threshold(n, theta, gamma, c, T):
    return c - phi(n, gamma) + reactance_term(n, theta, T)

def simulate_P(n_values, V, theta, gamma, c, T):
    P_values = []
    
    for n in n_values:
        S = threshold(n, theta, gamma, c, T)
        adoption = V >= S
        P_values.append(np.mean(adoption))
    
    return np.array(P_values)

# =========================================================
# 2. Paramètres du modèle
# =========================================================

N_agents = 20000

gamma = 2.0
c = 1.5
T = 1.0

# Motivations V_i ~ normale tronquée à 0
V = np.random.normal(loc=2.0, scale=0.8, size=N_agents)
V = np.maximum(V, 0)

# Réactance theta_i ~ Gamma
theta = np.random.gamma(shape=2.0, scale=1.0, size=N_agents)

# Grille de n
n_values = np.linspace(0, 10, 200)

# =========================================================
# 3. Simulation
# =========================================================

P_values = simulate_P(n_values, V, theta, gamma, c, T)

# =========================================================
# 4. Graphique
# =========================================================

plt.figure()
plt.plot(n_values, P_values)
plt.xlabel("Intensité du nudge (n)")
plt.ylabel("Proportion d'adoption P(n)")
plt.title("Simulation de P(n)")
plt.show()

#Deux scénarios
theta_high = np.random.gamma(shape=4.0, scale=1.5, size=N_agents)
P_high = simulate_P(n_values, V, theta_high, gamma, c, T)

plt.figure()
plt.plot(n_values, P_values, label="Réactance modérée")
plt.plot(n_values, P_high, label="Réactance forte")
plt.legend()
plt.xlabel("n")
plt.ylabel("P(n)")
plt.show()


#n optimal
n_star = n_values[np.argmax(P_values)]
P_star = np.max(P_values)

print("n optimal =", n_star)
print("P maximal =", P_star)

#variation T
import pandas as pd
T = [0.0,0.5,1.0,1.5,2.0]

liste_val = []

for val in T:
    P_values = simulate_P(n_values, V, theta, gamma, c, val)
    df = pd.DataFrame(P_values)
    df["T"] = val
    df["n"] = n_values
    liste_val.append(df)

final = pd.concat(liste_val)
final = final.rename(columns = {0:"val_p"})

import seaborn as sns
ax = sns.lineplot(data=final, x='n', y='val_p', hue='T', palette='viridis', 
    linewidth=2.5)

ax.set_title("Réactance en fonction de la valeur de T", fontsize=15, fontweight='bold')
ax.set_xlabel("n", fontsize=12)
ax.set_ylabel("P(n)", fontsize=12)

plt.tight_layout()
plt.show()  


########GRAPH 3D

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Grilles
n_values = np.linspace(0, 10, 100)
T_values = np.linspace(0.2, 3, 50)

N_agents = 20000
gamma = 2.0
c = 1.5

# Tirage une seule fois (important pour cohérence)
V = np.random.normal(loc=2.0, scale=0.8, size=N_agents)
V = np.maximum(V, 0)
theta = np.random.gamma(shape=2.0, scale=1.0, size=N_agents)

# Stockage
P_surface = np.zeros((len(T_values), len(n_values)))

for i, T in enumerate(T_values):
    for j, n in enumerate(n_values):
        phi = gamma * np.log(1 + n)
        S = c - phi + theta * np.tanh(n / T)
        P_surface[i, j] = np.mean(V >= S)

# Mesh
N, TT = np.meshgrid(n_values, T_values)

# Plot 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(N, TT, P_surface)

ax.set_xlabel("n")
ax.set_ylabel("T")
ax.set_zlabel("P(n,T)")
plt.show()


####HEATMAP

plt.figure()
plt.imshow(P_surface,
           extent=[n_values.min(), n_values.max(),
                   T_values.min(), T_values.max()],
           aspect='auto',
           origin='lower')

plt.colorbar(label="P(n,T)")
plt.xlabel("n")
plt.ylabel("T")
plt.title("Heatmap de la proportion d'adoption")
plt.show()

##HEATMAP n opti
n_star = []

for i in range(len(T_values)):
    idx_max = np.argmax(P_surface[i, :])
    n_star.append(n_values[idx_max])

n_star = np.array(n_star)

plt.figure()
plt.plot(T_values, n_star)
plt.xlabel("T")
plt.ylabel("n* optimal")
plt.title("Niveau optimal de nudge selon la confiance T")
plt.show()

