# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 15:38:47 2026

@author: basti
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from model import simulate


st.title("Simulation modèle Nudge - Réactance")


# ------------------------
# Paramètres
# ------------------------

st.sidebar.header("Paramètres")


N = st.sidebar.slider(
    "Nombre d'agents",
    1000,
    50000,
    10000
)


c = st.sidebar.slider(
    "Coût initial c",
    0.1,
    5.0,
    1.0
)


gamma_phi = st.sidebar.slider(
    "Force matérielle gamma",
    0.1,
    3.0,
    1.0
)


T = st.sidebar.slider(
    "Confiance institutionnelle T",
    0.1,
    3.0,
    1.0
)


alpha = st.sidebar.slider(
    "Non-linéarité réactance alpha",
    0.5,
    3.0,
    1.5
)



st.sidebar.subheader("Motivation")


V_mean = st.sidebar.slider(
    "Moyenne V",
    0.0,
    5.0,
    1.0
)


V_std = st.sidebar.slider(
    "Dispersion V",
    0.1,
    3.0,
    0.5
)


st.sidebar.subheader("Réactance")


st.sidebar.subheader("Population A")

theta_shape_A = st.sidebar.slider(
    "Shape Gamma A",
    0.1,
    10.0,
    1.0
)

theta_scale_A = st.sidebar.slider(
    "Scale Gamma A",
    0.01,
    1.0,
    0.05
)



st.sidebar.subheader("Population B")

theta_shape_B = st.sidebar.slider(
    "Shape Gamma B",
    0.1,
    10.0,
    2.0
)

theta_scale_B = st.sidebar.slider(
    "Scale Gamma B",
    0.01,
    1.0,
    0.2
)

# ------------------------
# Simulation
# ------------------------


n_values = range(0,100)


results_A = simulate(
    N,
    n_values,
    c,
    gamma_phi,
    T,
    alpha,
    V_mean,
    V_std,
    theta_shape_A,
    theta_scale_A
)


results_B = simulate(
    N,
    n_values,
    c,
    gamma_phi,
    T,
    alpha,
    V_mean,
    V_std,
    theta_shape_B,
    theta_scale_B
)

df_A = pd.DataFrame(results_A)

df_B = pd.DataFrame(results_B)

# ------------------------
# Graphiques
# ------------------------


st.subheader("Adoption selon intensité du nudge")

  
fig, ax = plt.subplots()

ax.plot(
    df_A["n"],
    df_A["adoption"],
    label="Population A"
)


ax.plot(
    df_B["n"],
    df_B["adoption"],
    label="Population B"
)


ax.legend()

ax.set_xlabel("n")
ax.set_ylabel("Taux adoption")
ax.grid(True)

n_opt_A = df_A.loc[df_A["adoption"].idxmax(),"n"]
n_opt_B = df_B.loc[df_B["adoption"].idxmax(),"n"]

ax.axvline(
    n_opt_A,
    linestyle="--",
    label=f"n*={n_opt_A}"
)
ax.axvline(
    n_opt_B,
    linestyle="--",
    label=f"n*={n_opt_B}",
    color = "r"
    )


ax.legend()

st.pyplot(fig)



st.subheader("Gain matériel vs Réactance population A")


fig, ax = plt.subplots()


ax.plot(
    df_A["n"],
    df_A["phi"],
    label="Gain matériel"
)

ax.plot(
    df_A["n"],
    df_A["reactance"],
    label="Réactance"
)


ax.legend()
ax.grid(True)


st.pyplot(fig)

st.subheader("Gain matériel vs Réactance population B")


fig, ax = plt.subplots()


ax.plot(
    df_B["n"],
    df_B["phi"],
    label="Gain matériel"
)

ax.plot(
    df_B["n"],
    df_B["reactance"],
    label="Réactance"
)


ax.legend()
ax.grid(True)


st.pyplot(fig)