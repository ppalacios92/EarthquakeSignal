"""
Description:
    This module provides a class for identifying the horizontal and vertical components
    of a seismic signal based on RMS (Root Mean Square) energy.

    The method assumes that the record contains exactly 3 signals, where the vertical
    component is typically the one with the lowest RMS value.

Date:
    2025-05-01
"""

__author__ = "Ing. Patricio Palacios B., M.Sc."
__version__ = "1.0.0"

import numpy as np

class SignalComponentIdentifier:
    """
    Identifies the V, H1, and H2 components in a set of 3 seismic signals based on RMS.
    """

    @staticmethod
    def identify(signals: dict):
        if len(signals) != 3:
            raise ValueError("Exactly 3 signals are required to identify components.")

        rms_values = {}
        for name, signal in signals.items():
            rms = np.sqrt(np.mean(signal**2))
            rms_values[name] = rms

        # Sort signals by RMS (ascending): lowest is likely vertical
        sorted_signals = sorted(rms_values.items(), key=lambda x: x[1])
        vertical_name = sorted_signals[0][0]
        horizontal_names = [sorted_signals[1][0], sorted_signals[2][0]]

        identified = {
            'V': signals[vertical_name],
            'H1': signals[horizontal_names[0]],
            'H2': signals[horizontal_names[1]],
        }

        names = {
            'V': vertical_name,
            'H1': horizontal_names[0],
            'H2': horizontal_names[1]
        }

        return identified, names
