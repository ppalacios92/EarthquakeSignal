"""
Description:
    This module contains the EarthquakeSummary class, which prints a summary of the key
    properties of a processed earthquake signal, including time step, duration,
    number of samples, RMS values, and associated filenames for each component.

Date:
    2025-05-01
"""

__author__ = "Ing. Patricio Palacios B., M.Sc."
__version__ = "1.0.0"

import numpy as np
import os

class EarthquakeSummary:
    """
    Utility class to display basic information about an EarthquakeSignal object.
    """

    def __init__(self, eq):
        """
        Parameters
        ----------
        eq : EarthquakeSignal
            Instance of the EarthquakeSignal class containing loaded seismic data.
        """
        self.eq = eq

    def print_summary(self):
        """
        Print a summary of the seismic signal's metadata and statistics,
        including time step, duration, RMS, and file names for H1, H2, and V.
        """
        print(f"\n{'='*30}")
        print(f"📌 Earthquake ID: {self.eq.name}")
        print(f"Sampling interval (dt): {self.eq.dt:.6f} s")
        n_samples = len(next(iter(self.eq.signals.values())))
        duration = self.eq.dt * n_samples
        print(f"Number of samples: {n_samples}")
        print(f"Total duration: {duration:.2f} s")
        print("Component information:")

        for comp in ['H1', 'H2', 'V']:
            sig = self.eq.signals[comp]
            rms = np.sqrt(np.mean(sig**2))
            fname = self.eq.component_names[comp]
            print(f"  - {comp}: file='{fname}', RMS={rms:.4e}")
        print(f"{'='*30}\n")
