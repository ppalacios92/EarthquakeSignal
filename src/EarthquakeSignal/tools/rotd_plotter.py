import numpy as np
import matplotlib.pyplot as plt

class RotDPlotter:
    """
    Utility class to generate acceleration orbit plots and overlay
    RotD direction lines based on angles from the RotD analysis.
    """

    def __init__(self, eq):
        """
        Parameters
        ----------
        eq : EarthquakeSignal
            Instance of EarthquakeSignal with corrected accelerations and RotD results.
        """
        self.eq = eq

    def plot_rotd(self):
        """
        Plot the acceleration orbit (H1 vs H2) and overlay RotD00, RotD50, and RotD100 angles.
        Also plot the response spectra in an adjacent subplot with all annotations and legend.
        """
        a1 = self.eq.corrected_acc['H1']
        a2 = self.eq.corrected_acc['H2']
        T = self.eq.rotd['T']
        psa_h1 = self.eq.newmark_spectra['H1']['PSa']
        psa_h2 = self.eq.newmark_spectra['H2']['PSa']
        psa_00 = self.eq.rotd['ROTD00']
        psa_50 = self.eq.rotd['ROTD50']
        psa_100 = self.eq.rotd['ROTD100']
        angle_00 = self.eq.rotd['angle_rotd00']
        angle_50 = self.eq.rotd['angle_rotd50']
        angle_100 = self.eq.rotd['angle_rotd100']

        pga_h1 = np.max(np.abs(a1))
        pga_h2 = np.max(np.abs(a2))
        pga_00 = np.max(psa_00)
        pga_50 = np.max(psa_50)
        pga_100 = np.max(psa_100)

        theta_00 = angle_00[0] if isinstance(angle_00, (list, np.ndarray)) else angle_00
        theta_50 = angle_50[0] if isinstance(angle_50, (list, np.ndarray)) else angle_50
        theta_100 = angle_100[0] if isinstance(angle_100, (list, np.ndarray)) else angle_100

        fig, axs = plt.subplots(1, 2, figsize=(15, 4))

        # Subplot 1: Response Spectra
        axs[0].plot(T, psa_h1, '--', linewidth=1.2, color=[0.5, 0.5, 0.5], label=f"{self.eq.component_names['H1']} (PGA={pga_h1:.3f}g)")
        axs[0].plot(T, psa_h2, '--', linewidth=1.2, color=[0.3, 0.3, 0.3], label=f"{self.eq.component_names['H2']} (PGA={pga_h2:.3f}g)")
        axs[0].plot(T, psa_100, '-', color='red', linewidth=1.5, label=f"RotD100 ({theta_100}°) (PGA={pga_100:.3f}g)")
        axs[0].plot(T, psa_50, '--', color=[0, 0.45, 0.74], linewidth=1.5, label=f"RotD50 ({theta_50}°) (PGA={pga_50:.3f}g)")
        axs[0].plot(T, psa_00, '--', color=[0.2, 0.6, 0], linewidth=1.5, label=f"RotD00 ({theta_00}°) (PGA={pga_00:.3f}g)")

        axs[0].set_title(self.eq.name, fontsize=10, fontweight='bold')
        axs[0].set_xlabel('Period [sec]', fontsize=9, fontweight='bold')
        axs[0].set_ylabel('Ag [g]', fontsize=9, fontweight='bold')
        axs[0].grid(True)
        axs[0].legend(fontsize=7)
        axs[0].set_xlim(left=0)

        # Subplot 2: Acceleration Orbit
        axs[1].plot(a1, a2, color='blue', linewidth=1.25, label='Acceleration Orbit')
        axs[1].axis('equal')

        # Define axis limits from data range
        lim_x = [np.min(a1) - 0.005, np.max(a1) + 0.005]
        x = np.linspace(lim_x[0], lim_x[1], 500)

        def plot_rotd_line(ax, theta_deg, style, color, label):
            theta_rad = np.deg2rad(theta_deg)
            y = np.tan(theta_rad) * x
            ax.plot(x, y, style, color=color, linewidth=1.2, label=label)

        plot_rotd_line(axs[1], theta_100, '-', 'red', f'RotD100 ({theta_100}°)')
        plot_rotd_line(axs[1], theta_50, '--', [0, 0.45, 0.74], f'RotD50 ({theta_50}°)')
        plot_rotd_line(axs[1], theta_00, '--', [0.2, 0.6, 0], f'RotD00 ({theta_00}°)')

        axs[1].set_xlim(lim_x)
        axs[1].set_ylim([np.min(a2) - 0.005, np.max(a2) + 0.005])
        axs[1].set_xlabel('H1 Acceleration [g]', fontsize=9, fontweight='bold')
        axs[1].set_ylabel('H2 Acceleration [g]', fontsize=9, fontweight='bold')
        axs[1].set_title('Acceleration Orbit', fontsize=10, fontweight='bold')
        axs[1].legend(fontsize=7)
        axs[1].grid(True)

        plt.show()
