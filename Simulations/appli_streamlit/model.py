# -*- coding: utf-8 -*-

import numpy as np
from scipy.stats import truncnorm, gamma


# ------------------------
# Fonctions du modèle
# ------------------------

def phi(n, gamma_phi):
    """
    Effet matériel du nudge
    """
    return gamma_phi * np.log(1+n)


def reactance(n, theta_i, T, alpha):
    """
    Coût psychologique lié à la réactance
    """
    return theta_i * (n/T)**alpha


def utility(Vi, theta_i, n, c, gamma_phi, T, alpha):

    return (
        Vi
        - c
        + phi(n, gamma_phi)
        - reactance(n, theta_i, T, alpha)
    )


# ------------------------
# Simulation population
# ------------------------

def simulate(
    N,
    n_values,
    c,
    gamma_phi,
    T,
    alpha,
    V_mean,
    V_std,
    theta_shape,
    theta_scale
):

    results = []

    # paramètres normale tronquée
    a = (-np.inf - V_mean) / V_std
    b = (np.inf - V_mean) / V_std


    # création agents

    Vi_agents = truncnorm.rvs(
        a,
        b,
        loc=V_mean,
        scale=V_std,
        size=N
    )


    theta_agents = gamma.rvs(
        a=theta_shape,
        scale=theta_scale,
        size=N
    )


    # boucle sur intensité du nudge

    for n in n_values:

        utilities = utility(
            Vi_agents,
            theta_agents,
            n,
            c,
            gamma_phi,
            T,
            alpha
        )

        adoption = np.mean(utilities > 0)

        results.append(
            {
            "n":n,
            "adoption":adoption,
            "phi":phi(n,gamma_phi),
            "reactance":np.mean(
                reactance(n,theta_agents,T,alpha)
            )
            }
        )


    return results

def simulate_population(
    N,
    n_values,
    c,
    gamma_phi,
    T,
    alpha,
    V_mean,
    V_std,
    theta_shape,
    theta_scale
):

    return simulate(
        N,
        n_values,
        c,
        gamma_phi,
        T,
        alpha,
        V_mean,
        V_std,
        theta_shape,
        theta_scale
    )