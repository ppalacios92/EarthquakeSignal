"""
Description:
    This module contains the EarthquakePlotter class, which is responsible for plotting
    the original seismic signal components (H1, H2, V) in a clean and readable format.

Date:
    2025-05-01
"""

__author__ = "Ing. Patricio Palacios B., M.Sc."
__version__ = "1.0.0"

import matplotlib.pyplot as plt
import numpy as np
import os

class EarthquakePlotter:
    """
    Utility class to generate plots for the original ground motion components of an earthquake.
    """

    def __init__(self, eq):
        """
        Parameters
        ----------
        eq : EarthquakeSignal
            Instance of EarthquakeSignal containing time step, signal data, and metadata.
        """
        self.eq = eq

    def plot_original_signals(self, save_svg=False):
        """
        Plot the original signals for H1, H2, and V in three horizontal subplots (1 row, 3 columns).
        All fonts are standardized for consistent visualization.
        """
        time = np.arange(len(next(iter(self.eq.signals.values())))) * self.eq.dt
        components = ['H1', 'H2', 'V']
        titles = ['H1', 'H2', 'V']

        fig, axs = plt.subplots(1, 3, figsize=(15, 3.5), sharex=True)

        for i, comp in enumerate(components):
            axs[i].plot(time, self.eq.signals[comp], label=f'{comp} - {self.eq.component_names[comp]}')
            axs[i].set_xlim(left=0)
            axs[i].set_xlabel('Time [s]', fontsize=9)
            axs[i].set_ylabel('Acceleration [g]', fontsize=9)
            axs[i].set_title(titles[i], fontweight='bold', fontsize=9)
            axs[i].legend(loc='upper right', fontsize=9)
            axs[i].tick_params(axis='both', labelsize=9)
            axs[i].grid(True)

        fig.suptitle(f'Original Ground Motions - {self.eq.name}', fontsize=11, fontweight='bold')
        
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
        output_path = os.path.join(project_root, 'outputs', self.eq.name)
        # --- Save to SVG if requested ---
        if save_svg:
            project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
            output_path = os.path.join(project_root, 'outputs', self.eq.name)
            os.makedirs(output_path, exist_ok=True)
            file_path = os.path.join(output_path, "original_ground_motions.svg")
            plt.savefig(file_path, format="svg")
        

        plt.show()
