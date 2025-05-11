"""
Description:
    This module defines the EarthquakeComparisonPlotter class for visualizing
    original and baseline-corrected ground motion signals in terms of acceleration,
    velocity, and displacement for all components (H1, H2, V) in separate rows.

Date:
    2025-05-10
"""

__author__ = "Ing. Patricio Palacios B., M.Sc."
__version__ = "1.1.0"

import matplotlib.pyplot as plt
import numpy as np


class EarthquakeComparisonPlotter:
    """
    Utility class for plotting original vs corrected acceleration, velocity, and displacement.
    """

    def __init__(self, eq):
        """
        Parameters
        ----------
        eq : EarthquakeSignal
            Instance of EarthquakeSignal containing signal data and metadata.
        """
        self.eq = eq

    def plot_corrected_signals(self):
        """
        Plot comparison of original and corrected signals in three rows (H1, H2, V),
        each showing acceleration, velocity, and displacement.
        """
        components = ['H1', 'H2', 'V']
        time = np.arange(len(self.eq.signals['H1'])) * self.eq.dt

        fig, axs = plt.subplots(3, 3, figsize=(15, 9), sharex=True)
        fig.suptitle(f'Signal Treatment - {self.eq.name}', fontsize=13, fontweight='bold')

        for row, comp in enumerate(components):
            # Convert acceleration to m/s²
            acc_raw = self.eq.signals[comp] * 9.81

            # Integrate to velocity and displacement (original)
            vel_raw = np.cumsum((acc_raw[:-1] + acc_raw[1:]) / 2) * self.eq.dt
            vel_raw = np.insert(vel_raw, 0, 0.0)

            disp_raw = np.zeros_like(acc_raw)
            for i in range(1, len(acc_raw)):
                disp_raw[i] = disp_raw[i-1] + vel_raw[i-1]*self.eq.dt + (2*acc_raw[i-1] + acc_raw[i])*self.eq.dt**2/6

            # Corrected signals
            acc_corr = self.eq.corrected_acc[comp]
            vel_corr = self.eq.corrected_vel[comp]
            disp_corr = self.eq.corrected_disp[comp]

            # Aceleración
            axs[row, 0].plot(time, acc_raw / 9.81, linestyle='--', color='gray', linewidth=0.8, label='Original')
            axs[row, 0].plot(time, acc_corr, color='blue', linewidth=0.8, label='Corrected')
            axs[row, 0].set_ylabel('g', fontsize=9)
            axs[row, 0].set_title(f'{comp} - Acceleration', fontsize=10, fontweight='bold')
            axs[row, 0].legend(fontsize=8)
            axs[row, 0].grid(True)
            axs[row, 0].tick_params(axis='both', labelsize=8)

            # Velocidad
            axs[row, 1].plot(time, vel_raw, linestyle='--', color='gray', linewidth=0.8, label='Original')
            axs[row, 1].plot(time, vel_corr, color='blue', linewidth=0.8, label='Corrected')
            axs[row, 1].set_ylabel('m/s', fontsize=9)
            axs[row, 1].set_title(f'{comp} - Velocity', fontsize=10, fontweight='bold')
            axs[row, 1].legend(fontsize=8)
            axs[row, 1].grid(True)
            axs[row, 1].tick_params(axis='both', labelsize=8)

            # Desplazamiento
            axs[row, 2].plot(time, disp_raw, linestyle='--', color='gray', linewidth=0.8, label='Original')
            axs[row, 2].plot(time, disp_corr, color='blue', linewidth=0.8, label='Corrected')
            axs[row, 2].set_ylabel('m', fontsize=9)
            axs[row, 2].set_title(f'{comp} - Displacement', fontsize=10, fontweight='bold')
            axs[row, 2].legend(fontsize=8)
            axs[row, 2].grid(True)
            axs[row, 2].tick_params(axis='both', labelsize=8)

        for col in range(3):
            axs[2, col].set_xlabel('Time [s]', fontsize=9)

        plt.subplots_adjust(hspace=0.4, wspace=0.25)
        plt.show()
