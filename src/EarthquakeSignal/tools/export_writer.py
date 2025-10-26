"""
Description:
    This module provides a class to export original and/or corrected
    seismic acceleration signals (H1, H2, V), as well as Newmark-corrected
    response spectra to plain text files.

    Each exported file contains two columns:
    - For time histories: time (s), acceleration (g)
    - For spectra: period (s), spectral acceleration (g)

    Output folder:
    outputs/<earthquake name>/

Date:
    2025-05-20
"""

__author__ = "Ing. Patricio Palacios B., M.Sc."
__version__ = "1.3.0"

import os
import numpy as np


class ExportWriter:
    """
    Class for exporting ground motion signals and spectra from EarthquakeSignal instance.
    """

    def __init__(self, eq):

        self.eq = eq


    def export(self, uncorrected=True, corrected=False, newmark_corrected=False):
        self.output_path = os.path.join(
            os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')),
            'outputs', self.eq.name
        )
        os.makedirs(self.output_path, exist_ok=True)

        self.component_map = {'H1': 'N', 'H2': 'E', 'V': 'Z'}


        if uncorrected:
            self._export_time_series(self.eq.signals, suffix='')

        if corrected:
            if not self.eq.corrected_acc:
                raise ValueError("Corrected acceleration data not found.")
            self._export_time_series(self.eq.corrected_acc, suffix='_acc_cor')

        if newmark_corrected:
            if not self.eq.newmark_spectra:
                raise ValueError("Newmark spectra data not found.")
            self._export_spectra(self.eq.newmark_spectra, suffix='_spectra_cor')


        if self.eq.rotd:
            self._export_rotd_spectra()


    def _export_time_series(self, signal_dict, suffix):
        n = len(next(iter(signal_dict.values())))
        time = np.arange(0, n * self.eq.dt, self.eq.dt)

        for comp, label in self.component_map.items():
            if comp not in signal_dict:
                continue
            data = signal_dict[comp]
            filename = f"{self.eq.component_names[comp]}_{label}{suffix}.txt"
            filepath = os.path.join(self.output_path, filename)
            with open(filepath, 'w') as f:
                for t, a in zip(time, data):
                    f.write(f"{t:.6f}\t{a:.6e}\n")

    def _export_spectra(self, spectra_dict, suffix):

        for comp, label in self.component_map.items():
            if comp not in spectra_dict:
                continue
            spec = spectra_dict[comp]
            T = spec.get('T', None)
            Sa = spec.get('Sa_corr', None)
            if T is None or Sa is None:
                continue

            filename = f"{self.eq.component_names[comp]}_{label}{suffix}.txt"
            filepath = os.path.join(self.output_path, filename)
            with open(filepath, 'w') as f:
                for t, sa in zip(T, Sa):
                    f.write(f"{t:.6f}\t{sa:.6e}\n")


    def _export_rotd_spectra(self):
        """Export RotD spectra to files."""
        rotd_path = os.path.join(self.output_path, 'rotd_spectra')
        os.makedirs(rotd_path, exist_ok=True)
        
        T = self.eq.rotd['T']
        
        spectra_map = {
            'ROTD00': self.eq.rotd['ROTD00'],
            'ROTD50': self.eq.rotd['ROTD50'],
            'ROTD100': self.eq.rotd['ROTD100'],
            'GeoMean': self.eq.rotd['PSa_geo_mean'],
            'ArithMean': self.eq.rotd['PSa_arith_mean'],
            'SRSS': self.eq.rotd['PSa_SRSS']
        }
        
        for name, Sa in spectra_map.items():
            filename = f"{self.eq.name}_{name}.txt"
            filepath = os.path.join(rotd_path, filename)
            with open(filepath, 'w') as f:
                for t, sa in zip(T, Sa):
                    f.write(f"{t:.6f}\t{sa:.6e}\n")