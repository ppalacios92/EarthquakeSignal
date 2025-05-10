"""
Description:
    This module defines the AriasIntensityAnalyzer class which computes the Arias intensity
    curve (normalized), significant duration, and start/end times based on a given
    acceleration signal and time step.

Date:
    2025-05-01
"""

__author__ = "Ing. Patricio Palacios B., M.Sc."
__version__ = "1.0.0"

import numpy as np

class AriasIntensityAnalyzer:
    """
    Static utility class to compute Arias intensity curve and significant duration.
    """

    @staticmethod
    def compute(signal, dt):
        """
        Compute Arias intensity and significant duration (5%–95%).

        Parameters
        ----------
        signal : np.ndarray
            Acceleration signal in units of [m/s^2].
        dt : float
            Time step in seconds.

        Returns
        -------
        IA_percent : np.ndarray
            Normalized Arias intensity (0–100%) as a function of time.
        t_start : float
            Time at 5% Arias intensity [s].
        t_end : float
            Time at 95% Arias intensity [s].
        ia_total : float
            Total Arias intensity [m/s].
        pot_dest : float
            Destructiveness potential as defined by energy over zero-crossing frequency squared.
        """
        g = 9.81
        t = np.arange(len(signal)) * dt

        # Arias intensity curve (non-normalized)
        IA = (np.pi / (2 * g)) * np.cumsum(signal**2) * dt
        ia_total = IA[-1]

        # Normalized to 100%
        IA_percent = 100 * IA / ia_total

        # Significant duration (5%–95%)
        idx5 = np.argmax(IA_percent >= 5)
        idx95 = np.argmax(IA_percent >= 95)
        t_start = t[idx5]
        t_end = t[idx95]

        # Count zero crossings
        cont_pd = np.count_nonzero(np.diff(np.sign(signal)))
        freq_cross = cont_pd / t[-1] if t[-1] > 0 else 0

        # Destructiveness potential
        pot_dest = ia_total / (freq_cross**2) if freq_cross > 0 else 0

        return IA_percent, t_start, t_end, ia_total, pot_dest
