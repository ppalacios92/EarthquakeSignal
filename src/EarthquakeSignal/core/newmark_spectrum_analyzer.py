"""
Description:
    This module defines the NewmarkSpectrumAnalyzer class, which implements the linear acceleration
    method (β-Newmark) to compute the response spectrum of a single-degree-of-freedom (SDOF) system
    subject to a ground acceleration record. The output includes spectral quantities and time histories.

Date:
    2025-05-01
"""

__author__ = "Ing. Patricio Palacios B., M.Sc."
__version__ = "1.0.1"

import numpy as np
from scipy.integrate import cumtrapz

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
            Ground acceleration array [m/s²].
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
        gama = 1 / 2
        beta = 1 / 6

        # Periods
        T = np.arange(0.00, 5.01, 0.1)

        # Convert acceleration to m/s² if needed
        ag = np.asarray(ag) * 9.81  # Assuming input is in g

        # Ground velocity and displacement (for completeness, not used in solver)
        vg = cumtrapz(ag, dx=dt, initial=0)
        ug = cumtrapz(vg, dx=dt, initial=0)

        # Initialize response spectra
        Sd, Sv, Sa, PSv, PSa = [], [], [], [], []

        # Initialize placeholders for one set of time histories
        u_hist, v_hist, a_hist, at_hist = [], [], [], []

        # Stability limit
        q = dt * np.pi * np.sqrt(2) * np.sqrt(gama - 2 * beta)

        for Tj in T:
            if Tj > q:
                w = 2 * np.pi / Tj
                m = 1.0
                k = m * w ** 2
                c = 2 * m * w * zeta

                # Newmark coefficients
                a1 = m / (beta * dt ** 2) + c * gama / (beta * dt)
                a2 = m / (beta * dt) + c * (gama / beta - 1)
                a3 = m * (1 / (2 * beta) - 1) + c * dt * (gama / (2 * beta) - 1)
                kp = k + a1

                # Initialize time histories
                u = np.zeros_like(ag)
                v = np.zeros_like(ag)
                a = np.zeros_like(ag)
                at = np.zeros_like(ag)

                # Newmark iteration
                for i in range(len(ag) - 1):
                    p_eff = -m * ag[i] + a1 * u[i] + a2 * v[i] + a3 * a[i]
                    u[i + 1] = p_eff / kp
                    a[i + 1] = (u[i + 1] - u[i]) / (beta * dt ** 2) - v[i] / (beta * dt) - a[i] * (1 / (2 * beta) - 1)
                    at[i + 1] = a[i + 1] + ag[i]  # Absolute acceleration
                    v[i + 1] = v[i] + dt * ((1 - gama) * a[i] + gama * a[i + 1])

                # Store max values
                Sd.append(np.max(np.abs(u)))
                Sv.append(np.max(np.abs(v)))
                Sa.append(np.max(np.abs(at)))
                PSv.append(w * Sd[-1])
                PSa.append(w ** 2 * Sd[-1])

                # Save one example time history (for T ≈ 1.0 s)
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

        # Convert lists to arrays
        Sd = np.array(Sd)
        Sv = np.array(Sv)
        Sa = np.array(Sa)
        PSv = np.array(PSv)
        PSa = np.array(PSa)

        # Convert output to [g] when needed
        PSa /= 9.81
        Sa /= 9.81
        a_hist = np.array(a_hist) / 9.81
        at_hist = np.array(at_hist) / 9.81

        return {
            'T': T,
            'PSa': PSa,
            'PSv': PSv,
            'Sd': np.array(Sd),
            'Sv': np.array(Sv),
            'Sa': Sa,
            'u': np.array(u_hist),
            'v': np.array(v_hist),
            'a': a_hist,
            'at': at_hist
        }
