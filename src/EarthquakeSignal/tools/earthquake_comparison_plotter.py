"""
Description:
    This module defines the EarthquakeComparisonPlotter class for visualizing
    original and baseline-corrected ground motion signals in terms of acceleration,
    velocity, and displacement.

Date:
    2025-05-01
"""

__author__ = "Ing. Patricio Palacios B., M.Sc."
__version__ = "1.0.0"

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
        Plot comparison of original and corrected signals in three horizontal subplots:
        acceleration, velocity, and displacement (all from component H1).
        """
        comp = 'H1'
        time = np.arange(len(self.eq.signals[comp])) * self.eq.dt

        acc_raw = self.eq.signals[comp]*9.81

        vel_raw = np.cumsum((acc_raw[:-1] + acc_raw[1:]) / 2) * self.eq.dt
        vel_raw = np.insert(vel_raw, 0, 0.0)
        disp_raw = np.zeros_like(acc_raw)
        for i in range(1, len(acc_raw)):
            disp_raw[i] = disp_raw[i-1] + vel_raw[i-1]*self.eq.dt + (2*acc_raw[i-1] + acc_raw[i])*self.eq.dt**2/6

        acc_corr = self.eq.corrected_acc[comp]
        vel_corr = self.eq.corrected_vel[comp]
        disp_corr = self.eq.corrected_disp[comp]

        fig, axs = plt.subplots(1, 3, figsize=(15, 3.5), sharex=True)
        fig.suptitle(f'Signal Treatment - {self.eq.name}', fontsize=11, fontweight='bold')
        acc_raw=acc_raw/9.81
        axs[0].plot(time, acc_raw, linestyle='--', color='gray', linewidth=0.8, label='Original')
        axs[0].plot(time, acc_corr, color='blue', linewidth=0.8, label='Corrected')
        axs[0].set_xlim(left=0)
        axs[0].set_title('Acceleration', fontsize=10, fontweight='bold')
        axs[0].set_xlabel('Time [s]', fontsize=9)
        axs[0].set_ylabel('Acceleration [g]', fontsize=9)
        axs[0].legend(fontsize=9)
        axs[0].tick_params(axis='both', labelsize=9)
        axs[0].grid(True)

        axs[1].plot(time, vel_raw, linestyle='--', color='gray', linewidth=0.8, label='Original')
        axs[1].plot(time, vel_corr, color='blue', linewidth=0.8, label='Corrected')
        axs[1].set_xlim(left=0)
        axs[1].set_title('Velocity', fontsize=10, fontweight='bold')
        axs[1].set_xlabel('Time [s]', fontsize=9)
        axs[1].set_ylabel('Velocity [m/s]', fontsize=9)
        axs[1].legend(fontsize=9)
        axs[1].tick_params(axis='both', labelsize=9)
        axs[1].grid(True)

        axs[2].plot(time, disp_raw, linestyle='--', color='gray', linewidth=0.8, label='Original')
        axs[2].plot(time, disp_corr, color='blue', linewidth=0.8, label='Corrected')
        axs[2].set_xlim(left=0)
        axs[2].set_title('Displacement', fontsize=10, fontweight='bold')
        axs[2].set_xlabel('Time [s]', fontsize=9)
        axs[2].set_ylabel('Displacement [m]', fontsize=9)
        axs[2].legend(fontsize=9)
        axs[2].tick_params(axis='both', labelsize=9)
        axs[2].grid(True)
        plt.show()
