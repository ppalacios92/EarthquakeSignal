"""
Description:
    This module defines the NewmarkSpectrumAnalyzer class, which implements the linear acceleration
    method (β-Newmark) to compute the response spectrum of a single-degree-of-freedom (SDOF) system
    subject to a ground acceleration record. The output includes spectral quantities and time histories.

Date:
    2025-06-10
"""

__author__ = "Ing. Patricio Palacios B., M.Sc."
__version__ = "1.1.0"

import numpy as np
from scipy.integrate import cumtrapz
from numba import njit


@njit
def solve_newmark(ag, dt, zeta, Tj):
    gama = 1/2
    beta = 1/4
    w = 2 * np.pi / Tj
    m = 1.0
    k = m * w**2
    c = 2 * m * w * zeta
    a1 = m / (beta * dt ** 2) + c * gama / (beta * dt)
    a2 = m / (beta * dt) + c * (gama / beta - 1)
    a3 = m * (1 / (2 * beta) - 1) + c * dt * (gama / (2 * beta) - 1)
    kp = k + a1

    u = np.zeros(len(ag))
    v = np.zeros(len(ag))
    a = np.zeros(len(ag))
    at = np.zeros(len(ag))

    for i in range(len(ag) - 1):
        p_eff = -m * ag[i] + a1 * u[i] + a2 * v[i] + a3 * a[i]
        u[i + 1] = p_eff / kp
        a[i + 1] = (u[i + 1] - u[i]) / (beta * dt ** 2) - v[i] / (beta * dt) - a[i] * (1 / (2 * beta) - 1)
        at[i + 1] = a[i + 1] + ag[i]
        v[i + 1] = v[i] + dt * ((1 - gama) * a[i] + gama * a[i + 1])

    Sd = np.max(np.abs(u))
    Sv = np.max(np.abs(v))
    Sa = np.max(np.abs(at))
    PSv = w * Sd
    PSa = w ** 2 * Sd

    return Sd, Sv, Sa, PSv, PSa, u, v, a, at


class NewmarkSpectrumAnalyzer:
    """
    Static class to compute PSa, PSv, Sd, Sv, Sa, and the time histories u, v, a, at
    using the β-Newmark linear acceleration method.
    """

    @staticmethod
    def compute(ag, dt, zeta=0.05):
        """
        Compute the response spectrum using the β-Newmark method.

        Parameters
        ----------
        ag : np.ndarray
            Ground acceleration array [g].
        dt : float
            Time step [s].
        zeta : float
            Damping ratio (default is 5%).

        Returns
        -------
        dict
            Dictionary with:
                'T'   : np.ndarray, Periods [s]
                'PSa' : np.ndarray, Pseudo-acceleration spectrum [g]
                'PSv' : np.ndarray, Pseudo-velocity spectrum [m/s]
                'Sd'  : np.ndarray, Displacement spectrum [m]
                'Sv'  : np.ndarray, Velocity spectrum [m/s]
                'Sa'  : np.ndarray, Acceleration spectrum [g]
                'u'   : np.ndarray, Displacement time history [m]
                'v'   : np.ndarray, Velocity time history [m/s]
                'a'   : np.ndarray, Relative acceleration time history [m/s²]
                'at'  : np.ndarray, Absolute acceleration time history [m/s²]
        """
        T = np.arange(0.01, 5.01, 0.01)
        ag = np.asarray(ag) * 9.81  # convert from g to m/s²

        Sd, Sv, Sa, PSv, PSa = [], [], [], [], []
        u_hist, v_hist, a_hist, at_hist = [], [], [], []

        # Estabilidad mínima
        gama = 1/2
        beta = 1/4
        q = dt * np.pi * np.sqrt(2) * np.sqrt(gama - 2 * beta)

        for Tj in T:
            if Tj > q:
                Sd_, Sv_, Sa_, PSv_, PSa_, u, v, a, at = solve_newmark(ag, dt, zeta, Tj)
                Sd.append(Sd_)
                Sv.append(Sv_)
                Sa.append(Sa_)
                PSv.append(PSv_)
                PSa.append(PSa_)

                if np.isclose(Tj, 1.0, atol=0.01):
                    u_hist = u
                    v_hist = v
                    a_hist = a
                    at_hist = at
            else:
                PGA = np.max(np.abs(ag))
                Sd.append(0)
                Sv.append(0)
                Sa.append(PGA)
                PSv.append(0)
                PSa.append(PGA)

        # Convertir a arrays
        Sd = np.array(Sd)
        Sv = np.array(Sv)
        Sa = np.array(Sa) / 9.81
        PSv = np.array(PSv)
        PSa = np.array(PSa) / 9.81
        a_hist = np.array(a_hist) / 9.81
        at_hist = np.array(at_hist) / 9.81

        return {
            'T': T,
            'PSa': PSa,
            'PSv': PSv,
            'Sd': Sd,
            'Sv': Sv,
            'Sa': Sa,
            'u': np.array(u_hist),
            'v': np.array(v_hist),
            'a': a_hist,
            'at': at_hist
        }
