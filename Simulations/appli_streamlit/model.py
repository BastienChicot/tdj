# -*- coding: utf-8 -*-

import numpy as np
from scipy.stats import truncnorm, gamma


def phi(n, gamma_phi):

    return gamma_phi * np.log(1+n)



def reactance(n, theta_i, T, alpha):

    return theta_i * (n/T)**alpha

def motivation(
    Vi0,
    delta_V,
    beta_i,
    n,
    T
):

    return (
        Vi0
        + delta_V
        * (
            1
            - np.exp(-beta_i * n / T)
        )
    )

def utility(
    Vi0,
    theta_i,
    beta_i,
    n,
    c,
    gamma_phi,
    T,
    alpha,
    delta_V
):

    Vi = motivation(
        Vi0,
        delta_V,
        beta_i,
        n,
        T
    )

    return (
        Vi
        - c
        + phi(n, gamma_phi)
        - reactance(n, theta_i, T, alpha)
    )


def simulate(
    Vi_agents,
    theta_agents,
    beta_agents,
    n_values,
    c,
    gamma_phi,
    T,
    alpha,
    delta_V
):

    results = []

    for n in n_values:

        # motivation des agents
        Vi = motivation(
            Vi_agents,
            delta_V,
            beta_agents,
            n,
            T
        )

        # utilité
        utilities = utility(
            Vi_agents,
            theta_agents,
            beta_agents,
            n,
            c,
            gamma_phi,
            T,
            alpha,
            delta_V
        )

        adoption = np.mean(utilities > 0)

        results.append({

            "n": n,

            "adoption": adoption,

            "motivation": np.mean(Vi),

            "phi": phi(n, gamma_phi),

            "reactance": np.mean(
                reactance(
                    n,
                    theta_agents,
                    T,
                    alpha
                )
            )

        })

    return results


def generate_population(
    N,
    V_mean,
    V_std,
    theta_shape,
    theta_scale,
    beta_shape,
    beta_scale
):

    # ------------------------
    # Motivation intrinsèque
    # ------------------------

    a = (-np.inf - V_mean) / V_std
    b = (np.inf - V_mean) / V_std

    Vi_agents = truncnorm.rvs(
        a,
        b,
        loc=V_mean,
        scale=V_std,
        size=N
    )

    # ------------------------
    # Réactance
    # ------------------------

    theta_agents = gamma.rvs(
        a=theta_shape,
        scale=theta_scale,
        size=N
    )

    # ------------------------
    # Sensibilité à la campagne
    # ------------------------

    beta_agents = gamma.rvs(
        a=beta_shape,
        scale=beta_scale,
        size=N
    )

    return Vi_agents, theta_agents, beta_agents