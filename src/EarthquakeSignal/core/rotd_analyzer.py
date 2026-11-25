import numpy as np
from EarthquakeSignal.core.newmark_spectrum_analyzer import NewmarkSpectrumAnalyzer

class RotDSpectrumAnalyzer:
    """
    Compute ROTD response spectra from two orthogonal components by rotating the signals
    from 0° to 180°, evaluating the pseudo-acceleration spectrum at each angle.
    """

    @staticmethod
    def compute_rotd(H1, H2, dt, damping=0.05, angles=None):
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
        angles : np.ndarray, optional
            Rotation angle grid in degrees. Defaults to 0-175 deg every 5 deg
            (36 distinct orientations). Every PSa value is symmetric under
            theta -> theta+180 (negating the forcing negates the response and
            peaks are absolute values), so a full-circle grid such as
            `np.arange(0, 361, step)` can be passed (e.g. to line up with a
            signed-peak IM computed elsewhere): the percentiles use each
            orientation once, so RotD00/50/100 do not change.

        Returns
        -------
        dict
            Dictionary containing ROTD00, ROTD50, ROTD100, angles, and PSA matrix.
        """
        if angles is None:
            angles = np.arange(0, 180, 5)  # 0-175 deg: 180 deg is the same orientation as 0 deg
        psa_matrix = []

        for angle in angles:
            rot = np.cos(np.radians(angle)) * H1 + np.sin(np.radians(angle)) * H2
            result = NewmarkSpectrumAnalyzer.compute(rot, dt, damping)
            psa_matrix.append(result["PSa"])

        psa_matrix = np.array(psa_matrix).T  # Shape: (n_periods, len(angles))

        # percentiles over distinct orientations only (theta and theta + 180 give the
        # same PSa), so a 0-360 or 0-180 inclusive grid does not count one twice
        _, unique_idx = np.unique(np.round(np.mod(angles, 180), 9), return_index=True)
        psa_unique = psa_matrix[:, unique_idx]
        angles_unique = np.asarray(angles)[unique_idx]

        rotd00 = np.percentile(psa_unique, 0, axis=1)
        rotd50 = np.percentile(psa_unique, 50, axis=1)
        rotd100 = np.percentile(psa_unique, 100, axis=1)

        # angle whose PSa is closest to each percentile (the median is interpolated)
        idx00 = np.argmin(np.abs(psa_unique - rotd00[:, None]), axis=1)
        idx50 = np.argmin(np.abs(psa_unique - rotd50[:, None]), axis=1)
        idx100 = np.argmin(np.abs(psa_unique - rotd100[:, None]), axis=1)

        angle00 = angles_unique[idx00]
        angle50 = angles_unique[idx50]
        angle100 = angles_unique[idx100]

        # component combinations act on the spectra, not on the time series
        # (Boore et al., 2006): combining H1, H2 first gives a non-physical record
        psa1 = NewmarkSpectrumAnalyzer.compute(H1, dt, damping)["PSa"]
        psa2 = NewmarkSpectrumAnalyzer.compute(H2, dt, damping)["PSa"]
        gm_result = {"PSa": np.sqrt(psa1 * psa2)}
        am_result = {"PSa": 0.5 * (psa1 + psa2)}
        srss_result = {"PSa": np.sqrt(psa1**2 + psa2**2)}

        return {
            "T": result["T"],
            "angles": angles,
            "ROTD00": rotd00,
            "ROTD50": rotd50,
            "ROTD100": rotd100,
            "angle_rotd00": angle00,
            "angle_rotd50": angle50,
            "angle_rotd100": angle100,
            "PSa_matrix": psa_matrix,
            "PSa_geo_mean": gm_result["PSa"],
            "PSa_arith_mean": am_result["PSa"],
            "PSa_SRSS": srss_result["PSa"],
        }
