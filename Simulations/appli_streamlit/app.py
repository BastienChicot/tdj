import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from model import simulate, generate_population

st.set_page_config(
    page_title="Reactance Model",
    layout="wide"
)

def check_password():

    def password_entered():

        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["authenticated"] = True
        else:
            st.session_state["authenticated"] = False


    if "authenticated" not in st.session_state:
        st.text_input(
            "Mot de passe",
            type="password",
            on_change=password_entered,
            key="password"
        )

        return False

    elif st.session_state["authenticated"]:
        return True

    else:
        st.text_input(
            "Mot de passe",
            type="password",
            on_change=password_entered,
            key="password"
        )

        st.error("Mot de passe incorrect")
        return False



if not check_password():
    st.stop()

# ------------------
# Configuration
# ------------------
st.title("Modèle d'adoption des politiques publiques")

st.write(
"""
Prototype de simulation intégrant :
- hétérogénéité des motivations individuelles ;
- réactance comportementale ;
- confiance institutionnelle.
"""
)

st.write(
"""
Modèle d'adoption intégrant :
- motivation intrinsèque
- efficacité du nudge
- réactance psychologique
- confiance institutionnelle
"""
)


# ------------------
# Paramètres
# ------------------

st.sidebar.header("Paramètres population")


N = st.sidebar.slider(
    "Nombre d'agents",
    100,
    10000,
    1000
)


V_mean = st.sidebar.slider(
    "Motivation moyenne V",
    0.1,
    3.0,
    1.0
)


V_std = st.sidebar.slider(
    "Hétérogénéité V",
    0.1,
    2.0,
    0.5
)


theta_shape = st.sidebar.slider(
    "Réactance (shape Gamma)",
    0.1,
    10.0,
    2.0
)


theta_scale = st.sidebar.slider(
    "Réactance (scale Gamma)",
    0.01,
    2.0,
    0.25
)



st.sidebar.header("Politique publique")


c = st.sidebar.slider(
    "Coût initial",
    0.1,
    5.0,
    1.0
)


gamma_phi = st.sidebar.slider(
    "Efficacité du nudge γ",
    0.1,
    5.0,
    0.5
)


T = st.sidebar.slider(
    "Confiance institutionnelle T",
    0.1,
    10.0,
    1.0
)


alpha = st.sidebar.slider(
    "Réactivité α",
    0.1,
    5.0,
    1.5
)



# ------------------
# Population
# ------------------

Vi_agents, theta_agents = generate_population(
    N,
    V_mean,
    V_std,
    theta_shape,
    theta_scale
)


# ------------------
# Simulation
# ------------------

n_values = np.linspace(0,10,100)


results = simulate(
    Vi_agents,
    theta_agents,
    n_values,
    c,
    gamma_phi,
    T,
    alpha
)


df = pd.DataFrame(results)


# ------------------
# Graphique adoption
# ------------------

st.subheader("Evolution de l'adoption")


fig, ax = plt.subplots(figsize=(6,3))

ax.plot(
    df["n"],
    df["adoption"]
)

ax.set_xlabel("Intensité du nudge")
ax.set_ylabel("Part adoptante")

ax.grid(True)

st.pyplot(fig)



# ------------------
# Effets internes
# ------------------

col1, col2 = st.columns(2)


with col1:

    st.subheader("Effet matériel")

    fig, ax = plt.subplots(figsize=(4,3))

    ax.plot(
        df["n"],
        df["phi"]
    )

    ax.set_xlabel("n")
    ax.set_ylabel("phi(n)")

    ax.grid(True)

    st.pyplot(fig)



with col2:

    st.subheader("Réactance moyenne")

    fig, ax = plt.subplots(figsize=(4,3))

    ax.plot(
        df["n"],
        df["reactance"]
    )

    ax.set_xlabel("n")
    ax.set_ylabel("Réactance")

    ax.grid(True)

    st.pyplot(fig)



# ------------------
# Population
# ------------------

st.subheader("Population simulée")


fig, ax = plt.subplots(figsize=(6,3))

ax.scatter(
    Vi_agents,
    theta_agents,
    alpha=0.3
)

ax.set_xlabel("Motivation intrinsèque V")
ax.set_ylabel("Réactance θ")

ax.grid(True)

st.pyplot(fig)