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
import os

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

    def plot_newmark_spectra(self, save_svg=False):
        """
        Plot pseudo-acceleration (PSa), pseudo-velocity (PSv), and displacement (Sd) spectra
        in a single row with three columns. Each subplot includes the three components
        H1, H2, and V using consistent formatting. Original (uncorrected) spectra
        are shown as dashed gray lines, corrected in solid colors.
        """
        components = ['H1', 'H2', 'V']
        colors = {'H1': 'black', 'H2': 'red', 'V': 'blue'}

        fig, axs = plt.subplots(1, 3, figsize=(15, 3.5), sharex=True)

        for comp in components:
            data = self.eq.newmark_spectra.get(comp, None)

            T = data['T']
            axs[0].plot(T, data['PSa'], linestyle='--', color=[0.6, 0.6, 0.6], linewidth=1)
            axs[0].plot(T, data['PSa_corr'], color=colors[comp], linewidth=1.2, label=comp)

            axs[1].plot(T, data['PSv'], linestyle='--', color=[0.6, 0.6, 0.6], linewidth=1)
            axs[1].plot(T, data['PSv_corr'], color=colors[comp], linewidth=1.2, label=comp)

            axs[2].plot(T, data['Sd'], linestyle='--', color=[0.6, 0.6, 0.6], linewidth=1)
            axs[2].plot(T, data['Sd_corr'], color=colors[comp], linewidth=1.2, label=comp)

        # Acceleration spectrum
        axs[0].set_title('Acceleration Spectrum', fontweight='bold', fontsize=9)
        axs[0].set_xlabel('Period [s]', fontsize=9)
        axs[0].set_ylabel('PSa [g]', fontsize=9)
        axs[0].legend(fontsize=8)
        axs[0].tick_params(axis='both', labelsize=8)
        axs[0].set_xlim(left=0)
        axs[0].grid(True)

        # Velocity spectrum
        axs[1].set_title('Velocity Spectrum', fontweight='bold', fontsize=9)
        axs[1].set_xlabel('Period [s]', fontsize=9)
        axs[1].set_ylabel('PSv [m/s]', fontsize=9)
        axs[1].legend(fontsize=8)
        axs[1].tick_params(axis='both', labelsize=8)
        axs[1].set_xlim(left=0)
        axs[1].grid(True)

        # Displacement spectrum
        axs[2].set_title('Displacement Spectrum', fontweight='bold', fontsize=9)
        axs[2].set_xlabel('Period [s]', fontsize=9)
        axs[2].set_ylabel('Sd [m]', fontsize=9)
        axs[2].legend(fontsize=8)
        axs[2].tick_params(axis='both', labelsize=8)
        axs[2].set_xlim(left=0)
        axs[2].grid(True)

        fig.suptitle(f'Newmark Response Spectra - {self.eq.name}', fontsize=11, fontweight='bold')

        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
        output_path = os.path.join(project_root, 'outputs', self.eq.name)
        # --- Save to SVG if requested ---
        if save_svg:
            project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
            output_path = os.path.join(project_root, 'outputs', self.eq.name)
            os.makedirs(output_path, exist_ok=True)
            file_path = os.path.join(output_path, "newmark_response_spectra.svg")
            plt.savefig(file_path, format="svg")
        

        plt.show()
