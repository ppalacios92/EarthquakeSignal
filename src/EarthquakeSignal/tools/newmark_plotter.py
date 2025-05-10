"""
Description:
    This module defines the NewmarkPlotter class for visualizing the pseudo-acceleration,
    pseudo-velocity, and displacement spectra using results from the β-Newmark method.
    The response spectra are shown in a single-row layout with grouped curves per component.
    Each plot includes corrected signals and gray dashed lines for the original (uncorrected) signals.

Date:
    2025-05-01
"""

__author__ = "Ing. Patricio Palacios B., M.Sc."
__version__ = "1.0.1"

import matplotlib.pyplot as plt
from EarthquakeSignal.core.newmark_spectrum_analyzer import NewmarkSpectrumAnalyzer

class NewmarkPlotter:
    """
    Utility class to generate grouped response spectrum plots (PSa, PSv, Sd)
    for the three components (H1, H2, V) of an earthquake signal using
    the β-Newmark integration method.
    """

    def __init__(self, eq):
        """
        Parameters
        ----------
        eq : EarthquakeSignal
            Instance containing acceleration data and metadata for a single record.
        """
        self.eq = eq

    def plot_newmark_spectra(self, damping=0.05):
        """
        Plot pseudo-acceleration (PSa), pseudo-velocity (PSv), and displacement (Sd) spectra
        in a single row with three columns. Each subplot includes the three components
        H1, H2, and V using consistent formatting. Original (uncorrected) spectra
        are shown as dashed gray lines.

        Parameters
        ----------
        damping : float
            Damping ratio used in the Newmark integration (default is 5%).
        """
        components = ['H1', 'H2', 'V']
        colors = {'H1': 'black', 'H2': 'red', 'V': 'blue'}

        fig, axs = plt.subplots(1, 3, figsize=(15, 3.5), sharex=True)

        for comp in components:
            signal_or = self.eq.signals[comp]
            signal_cr = self.eq.corrected_acc[comp]
            dt = self.eq.dt

            spectra_or = NewmarkSpectrumAnalyzer.compute(signal_or, dt, damping)
            spectra_cr = NewmarkSpectrumAnalyzer.compute(signal_cr, dt, damping)

            T_cr = spectra_cr['T']
            T_or = spectra_or['T']

            # Acceleration spectrum
            axs[0].plot(T_or, spectra_or['PSa'], linestyle='--', color=[0.6, 0.6, 0.6], linewidth=1)
            axs[0].plot(T_cr, spectra_cr['PSa'], linewidth=1.2, color=colors[comp], label=comp)


            # Velocity spectrum
            axs[1].plot(T_or, spectra_or['PSv'], linestyle='--', color=[0.6, 0.6, 0.6], linewidth=1)
            axs[1].plot(T_cr, spectra_cr['PSv'], linewidth=1.2, color=colors[comp], label=comp)


            # Displacement spectrum
            axs[2].plot(T_or, spectra_or['Sd'], linestyle='--', color=[0.6, 0.6, 0.6], linewidth=1)
            axs[2].plot(T_cr, spectra_cr['Sd'], linewidth=1.2, color=colors[comp], label=comp)


        # Format: Acceleration spectrum
        axs[0].set_title('Acceleration Spectrum', fontweight='bold', fontsize=9)
        axs[0].set_xlabel('Period [s]', fontsize=9)
        axs[0].set_ylabel('PSa [g]', fontsize=9)
        axs[0].legend(fontsize=8)
        axs[0].tick_params(axis='both', labelsize=8)
        axs[0].set_xlim(left=0)
        axs[0].grid(True)

        # Format: Velocity spectrum
        axs[1].set_title('Velocity Spectrum', fontweight='bold', fontsize=9)
        axs[1].set_xlabel('Period [s]', fontsize=9)
        axs[1].set_ylabel('PSv [m/s]', fontsize=9)
        axs[1].legend(fontsize=8)
        axs[1].tick_params(axis='both', labelsize=8)
        axs[1].set_xlim(left=0)
        axs[1].grid(True)

        # Format: Displacement spectrum
        axs[2].set_title('Displacement Spectrum', fontweight='bold', fontsize=9)
        axs[2].set_xlabel('Period [s]', fontsize=9)
        axs[2].set_ylabel('Sd [m]', fontsize=9)
        axs[2].legend(fontsize=8)
        axs[2].tick_params(axis='both', labelsize=8)
        axs[2].set_xlim(left=0)
        axs[2].grid(True)

        fig.suptitle(f'Newmark Response Spectra - {self.eq.name}', fontsize=11, fontweight='bold')
        plt.show()
