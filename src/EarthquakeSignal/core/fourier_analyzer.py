"""
Description:
    This module defines the FourierAnalyzer class responsible for computing the frequency
    spectrum of a given acceleration signal using the Fast Fourier Transform (FFT).
    It also detects and returns the most dominant frequencies based on peak prominence and spacing.

Date:
    2025-05-01
"""

__author__ = "Ing. Patricio Palacios B., M.Sc."
__version__ = "1.0.0"

import numpy as np
from scipy.signal import find_peaks


class FourierAnalyzer:
    """
    Static utility class to compute the FFT spectrum and extract dominant frequency components.
    """

    @staticmethod
    def compute(signal: np.ndarray, dt: float, num_frequencies: int = 4):
        """
        Compute the power spectrum using FFT and extract the dominant frequencies and periods.

        Parameters
        ----------
        signal : np.ndarray
            Acceleration signal in units of [m/s²].
        dt : float
            Time step in seconds.
        num_frequencies : int
            Number of dominant frequencies to extract from the spectrum.

        Returns
        -------
        freqs : np.ndarray
            Frequency vector [Hz].
        Pyy : np.ndarray
            Power spectrum (amplitude squared) corresponding to the frequency vector.
        dom_freqs : np.ndarray
            List of the most dominant frequencies [Hz].
        dom_periods : np.ndarray
            Periods corresponding to the dominant frequencies [s].
        dom_peaks : np.ndarray
            Amplitude values of the selected dominant frequencies.
        """
        N = len(signal)
        Fs = 1.0 / dt

        # Frequency axis for the one-sided FFT
        freqs = Fs * np.arange(0, N // 2) / N

        # Compute FFT and one-sided power spectrum
        Y = np.fft.fft(signal)
        Pyy = np.abs(Y[:N // 2])**2 / N

        # Identify spectral peaks with minimum prominence and spacing
        peaks, properties = find_peaks(Pyy, prominence=1e-6, distance= int(len(Pyy) * 0.02))
        peak_amplitudes = Pyy[peaks]
        peak_freqs = freqs[peaks]

        # Sort and select the most prominent peaks
        sorted_indices = np.argsort(peak_amplitudes)[::-1]
        top_indices = sorted_indices[:num_frequencies]

        dom_freqs = peak_freqs[top_indices]
        dom_peaks = peak_amplitudes[top_indices]
        dom_periods = 1.0 / dom_freqs

        return freqs, Pyy, dom_freqs, dom_periods, dom_peaks
