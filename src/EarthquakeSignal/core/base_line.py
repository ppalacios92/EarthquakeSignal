"""
Description:
    This module defines the BaselineCorrection class, which provides static methods
    for removing baseline drift from seismic acceleration signals. It applies
    integration-based velocity and displacement calculations with a polynomial
    correction model for acceleration drift removal.

Date:
    2025-05-01
"""

__author__ = "Ing. Patricio Palacios B., M.Sc."
__version__ = "1.0.2"

import numpy as np

class BaselineCorrection:
    @staticmethod
    def apply(signal: np.ndarray, dt: float):
        """
        Apply baseline correction to a single acceleration signal.

        Parameters
        ----------
        signal : np.ndarray
            Raw acceleration time series in [g].
        dt : float
            Time step (sampling interval) in [s].

        Returns
        -------
        ai_corr : np.ndarray
            Corrected acceleration [g].
        vi_corr : np.ndarray
            Corrected velocity [m/s].
        di_corr : np.ndarray
            Corrected displacement [m].
        """
        # Convert input acceleration to m/s²
        signal = signal * 9.81

        dim1 = len(signal)
        time = np.arange(dim1) * dt

        # Step 1: Velocity integration
        vel = np.zeros(dim1)
        for i in range(1, dim1):
            vel[i] = vel[i-1] + (signal[i-1] + signal[i]) * dt / 2

        # Step 2: Displacement integration
        disp = np.zeros(dim1)
        for i in range(1, dim1):
            disp[i] = disp[i-1] + vel[i-1]*dt + (2*signal[i-1] + signal[i]) * dt**2 / 6

        # Step 3: Compute polynomial drift coefficients A1, A2, A3
        A1i, A2i, A3i = np.zeros(dim1-1), np.zeros(dim1-1), np.zeros(dim1-1)
        for i in range(dim1 - 1):
            ti, ti1 = time[i], time[i+1]
            vi = vel[i]
            ai, ai1 = signal[i], signal[i+1]
            dti = ti1 - ti

            A1i[i] = 0.5 * vi * dti * (ti + ti1) + (1/24) * dti**2 * (
                ai*(3*ti + 5*ti1) + ai1*(ti + 3*ti1))
            A2i[i] = (1/3) * vi * dti * (ti**2 + ti*ti1 + ti1**2) + (1/60) * dti**2 * (
                ai*(4*ti**2 + 7*ti*ti1 + 9*ti1**2) + ai1*(ti**2 + 3*ti*ti1 + 6*ti1**2))
            A3i[i] = (1/4) * vi * dti * (ti**3 + ti**2*ti1 + ti*ti1**2 + ti1**3) + (1/120) * dti**2 * (
                ai*(5*ti**3 + 9*ti**2*ti1 + 12*ti*ti1**2 + 14*ti1**3) +
                ai1*(ti**3 + 3*ti**2*ti1 + 6*ti*ti1**2 + 10*ti1**3))

        A1, A2, A3 = np.sum(A1i), np.sum(A2i), np.sum(A3i)
        tT = time[-1]

        # Step 4: Polynomial coefficients
        C0 = (300*A1/tT**3) - (900*A2/tT**4) + (630*A3/tT**5)
        C1 = (-900*A1/tT**4) + (2880*A2/tT**5) - (2100*A3/tT**6)
        C2 = (630*A1/tT**5) - (2100*A2/tT**6) + (1575*A3/tT**7)

        # Step 5: Apply corrections
        ai_corr = signal - (C0 + 2*C1*time + 3*C2*time**2)
        vi_corr = vel - (C0*time + C1*time**2 + C2*time**3)
        di_corr = disp - (0.5*C0*time**2 + (1/3)*C1*time**3 + 0.25*C2*time**4)

        # Convert corrected acceleration back to [g]
        ai_corr = ai_corr / 9.81

        return ai_corr, vi_corr, di_corr
