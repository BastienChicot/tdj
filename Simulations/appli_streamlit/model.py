# -*- coding: utf-8 -*-

import numpy as np
from scipy.stats import truncnorm, gamma


def phi(n, gamma_phi):

    return gamma_phi * np.log(1+n)



def reactance(n, theta_i, T, alpha):

    return theta_i * (n/T)**alpha



def utility(Vi, theta_i, n, c, gamma_phi, T, alpha):

    return (
        Vi
        - c
        + phi(n, gamma_phi)
        - reactance(n, theta_i, T, alpha)
    )



def simulate(
    Vi_agents,
    theta_agents,
    n_values,
    c,
    gamma_phi,
    T,
    alpha
):

    results = []


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
                "n": n,
                "adoption": adoption,
                "phi": phi(n, gamma_phi),
                "reactance": np.mean(
                    reactance(
                        n,
                        theta_agents,
                        T,
                        alpha
                    )
                )
            }
        )


    return results



def generate_population(
    N,
    V_mean,
    V_std,
    theta_shape,
    theta_scale
):

    a = (-np.inf - V_mean) / V_std
    b = (np.inf - V_mean) / V_std


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


    return Vi_agents, theta_agents