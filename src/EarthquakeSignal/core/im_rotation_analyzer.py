import numpy as np


class IMRotationAnalyzer:
    """
    Rotate the corrected acceleration/velocity/displacement pair (H1, H2)
    over a grid of angles and report the rotated peak intensity per angle,
    replicating the PGA/PGV/PGD "rose" of Hui et al. (Influence of velocity
    pulse directivity on seismic response of cross-fault bridges, Structures,
    2024/2025):

        f(t, theta) = f1(t)*cos(theta) + f2(t)*sin(theta)

    PGA(theta) and PGV(theta) use the absolute peak (max|.|), which is
    mathematically symmetric under theta -> theta+180 (negating the rotated
    signal negates its own values, so the absolute peak is unchanged) -- a
    0-360 sweep is a mirrored duplicate of 0-180 for these two. PGD is
    reported as a signed peak (max and min separately) because permanent
    displacement is not zero-mean like acceleration/velocity, so its signed
    extremes genuinely differ between theta and theta+180 -- this is the one
    quantity where the full 0-360 sweep carries information the 0-180 sweep
    does not.
    """

    @staticmethod
    def compute(acc1, acc2, vel1, vel2, disp1, disp2, angles=None):
        """
        Parameters
        ----------
        acc1, acc2 : np.ndarray
            Corrected acceleration of H1, H2.
        vel1, vel2 : np.ndarray
            Corrected velocity of H1, H2.
        disp1, disp2 : np.ndarray
            Corrected displacement of H1, H2.
        angles : np.ndarray, optional
            Rotation angle grid in degrees. Defaults to a full circle,
            0-360 deg every 5 deg (73 angles) -- unlike
            RotDSpectrumAnalyzer, the default here is the full sweep because
            PGD_theta_max/PGD_theta_min are only meaningful over 0-360.

        Returns
        -------
        dict
            'angles', 'PGA_theta', 'PGV_theta', 'PGD_theta_max', 'PGD_theta_min'.
        """
        if angles is None:
            angles = np.arange(0, 361, 5)

        n = len(angles)
        pga_theta = np.zeros(n)
        pgv_theta = np.zeros(n)
        pgd_theta_max = np.zeros(n)
        pgd_theta_min = np.zeros(n)

        for i, angle in enumerate(angles):
            c, s = np.cos(np.radians(angle)), np.sin(np.radians(angle))
            a_rot = c * acc1 + s * acc2
            v_rot = c * vel1 + s * vel2
            d_rot = c * disp1 + s * disp2

            pga_theta[i] = np.max(np.abs(a_rot))
            pgv_theta[i] = np.max(np.abs(v_rot))
            pgd_theta_max[i] = np.max(d_rot)
            pgd_theta_min[i] = np.min(d_rot)

        return {
            "angles": angles,
            "PGA_theta": pga_theta,
            "PGV_theta": pgv_theta,
            "PGD_theta_max": pgd_theta_max,
            "PGD_theta_min": pgd_theta_min,
        }
