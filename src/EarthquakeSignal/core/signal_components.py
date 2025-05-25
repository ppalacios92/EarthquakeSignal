"""
Description:
    This module provides a class for identifying the horizontal and vertical components
    of a seismic signal based on filename suffix or RMS (Root Mean Square) energy.

    Priority is given to filename-based identification when filenames end with
    _X, _Y, or _Z (before extension), corresponding to components H1, H2, and V.
    If this fails, fallback to energy-based identification is used.

Date:
    2025-05-10
"""

__author__ = "Ing. Patricio Palacios B., M.Sc."
__version__ = "1.2.1"

import numpy as np
import os


class SignalComponentIdentifier:
    """
    Identifies the V, H1, and H2 components in a set of 3 seismic signals.
    """

    @staticmethod
    def identify(signals: dict):
        """
        Identify the three seismic components: H1, H2, and V.

        Parameters
        ----------
        signals : dict
            Dictionary where keys are filenames and values are numpy arrays of the signals.

        Returns
        -------
        identified : dict
            Dictionary with keys 'H1', 'H2', 'V' and signal arrays as values.

        names : dict
            Dictionary mapping 'H1', 'H2', 'V' to the original filename keys (without extension).

        Raises
        ------
        ValueError
            If fewer or more than 3 signals are provided or identification fails.
        """
        if len(signals) != 3:
            raise ValueError("Exactly 3 signals are required to identify components.")

        identified = {}
        names = {}

        # --- Try to identify based on filename endings: _X, _Y, _Z ---
        filename_map = {'_X': 'H1', '_Y': 'H2', '_Z': 'V'}

        for key in signals.keys():
            basename = os.path.splitext(os.path.basename(key))[0]  # remove extension
            for suffix, label in filename_map.items():
                if basename.upper().endswith(suffix):
                    if label in identified:
                        raise ValueError(f"Duplicate component label detected for {label}")
                    identified[label] = signals[key]
                    names[label] = basename  # <- remove extension
                    break  # exit suffix loop once matched

        # --- Fallback to RMS-based identification if incomplete ---
        if len(identified) < 3:
            remaining = {
                name: signal for name, signal in signals.items()
                if os.path.splitext(os.path.basename(name))[0] not in names.values()
            }

            rms_values = {
                name: np.sqrt(np.mean(signal**2))
                for name, signal in remaining.items()
            }

            sorted_rms = sorted(rms_values.items(), key=lambda x: x[1])
            fallback_labels = [lbl for lbl in ['V', 'H1', 'H2'] if lbl not in identified]

            for (fname, _), label in zip(sorted_rms, fallback_labels):
                identified[label] = signals[fname]
                basename = os.path.splitext(os.path.basename(fname))[0]
                names[label] = basename  # <- again, without extension

        # --- Final validation ---
        if set(identified.keys()) != {'H1', 'H2', 'V'}:
            raise RuntimeError("Failed to assign all three components (H1, H2, V).")

        return identified, names
