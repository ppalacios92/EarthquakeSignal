import numpy as np
from EarthquakeSignal.core.newmark_spectrum_analyzer import NewmarkSpectrumAnalyzer

class RotDSpectrumAnalyzer:
    """
    Compute ROTD response spectra from two orthogonal components by rotating the signals
    from 0° to 180°, evaluating the pseudo-acceleration spectrum at each angle.
    """

    @staticmethod
    def compute_rotd(H1, H2, dt, damping=0.05):
        """
        Parameters
        ----------
        H1 : np.ndarray
            First horizontal component (e.g., NS).
        H2 : np.ndarray
            Second horizontal component (e.g., EW).
        dt : float
            Time step of the input signals.
        damping : float
            Damping ratio (default is 5%).

        Returns
        -------
        dict
            Dictionary containing ROTD00, ROTD50, ROTD100, angles, and PSA matrix.
        """
        angles = np.arange(0, 181, 5)
        psa_matrix = []

        for angle in angles:
            rot = np.cos(np.radians(angle)) * H1 + np.sin(np.radians(angle)) * H2
            result = NewmarkSpectrumAnalyzer.compute(rot, dt, damping)
            psa_matrix.append(result["PSa"])

        psa_matrix = np.array(psa_matrix).T  # Shape: (n_periods, 181)

        rotd00 = np.percentile(psa_matrix, 0, axis=1)
        rotd50 = np.percentile(psa_matrix, 50, axis=1)
        rotd100 = np.percentile(psa_matrix, 100, axis=1)

        idx00 = np.argmax(psa_matrix == rotd00[:, None], axis=1)
        idx50 = np.argmax(psa_matrix == rotd50[:, None], axis=1)
        idx100 = np.argmax(psa_matrix == rotd100[:, None], axis=1)

        angle00 = angles[idx00]
        angle50 = angles[idx50]
        angle100 = angles[idx100]

        geo_mean = np.sqrt(np.abs(H1 * H2))
        gm_result = NewmarkSpectrumAnalyzer.compute(geo_mean, dt, damping)

        arith_mean = 0.5 * (H1 + H2)
        am_result = NewmarkSpectrumAnalyzer.compute(arith_mean, dt, damping)

        return {
            "T": result["T"],
            "ROTD00": rotd00,
            "ROTD50": rotd50,
            "ROTD100": rotd100,
            "angle_rotd00": angle00,
            "angle_rotd50": angle50,
            "angle_rotd100": angle100,
            "PSa_matrix": psa_matrix,
            "PSa_geo_mean": gm_result["PSa"],
            "PSa_arith_mean": am_result["PSa"],
        }
