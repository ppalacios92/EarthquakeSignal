"""
Description:
    This module defines the FourierPlotter class for visualizing the frequency content
    of a signal using the FFT spectrum and highlighting dominant frequencies.

Date:
    2025-05-01
"""

__author__ = "Ing. Patricio Palacios B., M.Sc."
__version__ = "1.0.0"

import numpy as np
import matplotlib.pyplot as plt
from EarthquakeSignal.core.fourier_analyzer import FourierAnalyzer
import os

class FourierPlotter:
    """
    Utility class for plotting the FFT spectrum of the earthquake signal components.
    """

    def __init__(self, eq):
        """
        Parameters
        ----------
        eq : EarthquakeSignal
            Instance of EarthquakeSignal containing time step and signals.
        """
        self.eq = eq

    def plot_spectrum(self, num_frequencies=4 , save_svg=False):
        """
        Plot the FFT spectrum for all components (H1, H2, V) with dominant frequencies highlighted.

        Parameters
        ----------
        num_frequencies : int
            Number of dominant frequencies to annotate.
        """
        components = ['H1', 'H2', 'V']
        fig, axs = plt.subplots(3, 1, figsize=(15, 9), sharey=True)

        for i, comp in enumerate(components):
            signal = self.eq.signals[comp]
            dt = self.eq.dt

            freqs, Pyy, dom_freqs, dom_periods, dom_peaks = FourierAnalyzer.compute(signal, dt, num_frequencies)

            axs[i].semilogx(freqs, Pyy, linewidth=1.2, color='black')
            axs[i].scatter(dom_freqs, dom_peaks, color='blue', s=30, zorder=5)

            # Etiquetas f1, f2...
            for j, (f, A) in enumerate(zip(dom_freqs, dom_peaks)):
                axs[i].annotate(f"f{j+1}", xy=(f, A), xytext=(f, A * 1.05),
                                textcoords="data", fontsize=8,
                                ha='center',
                                arrowprops=dict(arrowstyle="->", lw=0.5, color='gray'))

            # Texto en cuadro blanco
            lines = [f"f{j+1} = {f:.2f} Hz / T = {T:.2f} s" for j, (f, T) in enumerate(zip(dom_freqs, dom_periods))]
            textstr = '\n'.join(lines)
            axs[i].text(0.98, 0.95, textstr,
                        transform=axs[i].transAxes,
                        fontsize=8,
                        verticalalignment='top',
                        horizontalalignment='right',
                        bbox=dict(facecolor='white', edgecolor='black'))

            axs[i].set_title(f"{comp} - {self.eq.component_names[comp]}", fontsize=10, fontweight='bold')
            if i == 2:
                axs[i].set_xlabel('Frequency [Hz]', fontsize=9)
            axs[i].tick_params(axis='both', labelsize=8)
            axs[i].grid(True, which='both')

            axs[i].set_ylabel('Power Amplitude', fontsize=9)
        fig.suptitle(f"FFT Spectrum with Dominant Frequencies - {self.eq.name}", fontsize=11, fontweight='bold')

        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
        output_path = os.path.join(project_root, 'outputs', self.eq.name)
        # --- Save to SVG if requested ---
        if save_svg:
            project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
            output_path = os.path.join(project_root, 'outputs', self.eq.name)
            os.makedirs(output_path, exist_ok=True)
            file_path = os.path.join(output_path, "fft_spectrum.svg")
            plt.savefig(file_path, format="svg")
        

        plt.show()
