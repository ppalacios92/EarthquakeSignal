"""
Description:
    This module defines the AriasPlotter class to generate plots of normalized Arias
    intensity and acceleration signals for each component (H1, H2, V) of an earthquake.
    The plots include significant duration (5%–95%) indicators and textual annotations.

Date:
    2025-05-01
"""

__author__ = "Ing. Patricio Palacios B., M.Sc."
__version__ = "1.0.0"

import matplotlib.pyplot as plt
import numpy as np

class AriasPlotter:
    """
    Utility class to plot Arias intensity curves and significant duration overlays
    for the three components (H1, H2, V) of an earthquake signal.
    """

    def __init__(self, eq):
        """
        Parameters
        ----------
        eq : EarthquakeSignal
            Instance of EarthquakeSignal containing signal, Arias intensity,
            and acceleration data.
        """
        self.eq = eq

    def plot_arias(self):
        """
        Plot Arias intensity (normalized) and acceleration signal for each component
        (H1, H2, V) including the significant duration region (5%–95%).
        """
        components = ['H1', 'H2', 'V']
        fig, axs = plt.subplots(3, 2, figsize=(15, 10), sharex='col')
        fig.suptitle(f'Arias Intensity and Acceleration with SD - {self.eq.name}', fontsize=11, fontweight='bold')

        for i, comp in enumerate(components):
            acc = self.eq.signals[comp]
            dt = self.eq.dt
            time = np.arange(len(acc)) * dt
            ia_info = self.eq.arias[comp]

            ia_percent = ia_info['IA_percent']
            t_start = ia_info['t_start']
            t_end = ia_info['t_end']
            ia_total = ia_info['IA_total']
            pot_dest = ia_info['pot_dest']

            # --- Plot of normalized Arias intensity ---
            axs[i, 0].plot(time, ia_percent, 'k-', linewidth=1.2)
            axs[i, 0].axvline(x=t_start, linestyle='--', color='red', linewidth=0.8)
            axs[i, 0].axvline(x=t_end, linestyle='--', color='red', linewidth=0.8)
            axs[i, 0].text(t_start+10*dt, 5, f"5%, t={t_start:.2f}s", fontsize=8)
            axs[i, 0].text(t_end+10*dt, 80, f"95%, t={t_end:.2f}s", fontsize=8)
            axs[i, 0].set_title(f'{comp} - Arias Intensity', fontsize=9, fontweight='bold')
            axs[i, 0].set_xlabel('Time [s]', fontsize=9)
            axs[i, 0].set_ylabel('I$_A$ [%]', fontsize=9)
            axs[i, 0].tick_params(axis='both', labelsize=8)
            axs[i, 0].set_xlim(left=0)
            axs[i, 0].grid(True)

            # --- Textbox with summary statistics ---
            box_text = '\n'.join([
                f"SD = {t_end - t_start:.2f} s",
                f"Ia = {ia_total:.3f} m/s",
                f"PD = {pot_dest * 100:.2f} cm-s"
            ])
            axs[i, 0].text(0.95, 0.5, box_text,
                           transform=axs[i, 0].transAxes,
                           fontsize=8, va='center', ha='right',
                           bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='black'))

            # --- Plot of acceleration with significant duration (SD) overlay ---
            axs[i, 1].plot(time, acc, color='black', linewidth=0.5, label='Original')
            mask = (time >= t_start) & (time <= t_end)
            axs[i, 1].plot(time[mask], acc[mask], color='red', linewidth=1.2, label='SD Segment')
            axs[i, 1].set_title(f'{comp} - Acceleration with SD', fontsize=9, fontweight='bold')
            axs[i, 1].set_xlabel('Time [s]', fontsize=9)
            axs[i, 1].set_ylabel('Acceleration [g]', fontsize=9)
            axs[i, 1].tick_params(axis='both', labelsize=8)
            axs[i, 1].legend(loc='upper right', fontsize=7)
            axs[i, 1].set_xlim(left=0)
            axs[i, 1].grid(True)
            
        plt.show()
