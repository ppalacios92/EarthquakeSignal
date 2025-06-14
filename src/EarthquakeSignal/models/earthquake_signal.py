"""
Description:
    This module defines the EarthquakeSignal class, which represents a single earthquake record.
    It handles reading, organizing, and optionally processing the seismic signals using helper
    modules for loading, identifying components, summarizing, plotting, and applying preprocessing
    operations such as baseline correction, Arias intensity computation, and frequency spectrum analysis.

Date:
    2025-05-01
"""

__author__ = "Ing. Patricio Palacios B., M.Sc."
__version__ = "1.0.0"

import os
import re
from EarthquakeSignal.core.signal_loader import SignalLoader
from EarthquakeSignal.core.signal_components import SignalComponentIdentifier
from EarthquakeSignal.core.base_line import BaselineCorrection
from EarthquakeSignal.core.arias_intensity import AriasIntensityAnalyzer
from EarthquakeSignal.core.fourier_analyzer import FourierAnalyzer
from EarthquakeSignal.core.newmark_spectrum_analyzer import NewmarkSpectrumAnalyzer
from EarthquakeSignal.core.rotd_analyzer import RotDSpectrumAnalyzer

from EarthquakeSignal.tools.earthquake_summary import EarthquakeSummary
from EarthquakeSignal.tools.earthquake_plotter import EarthquakePlotter
from EarthquakeSignal.tools.earthquake_comparison_plotter import EarthquakeComparisonPlotter
from EarthquakeSignal.tools.arias_plotter import AriasPlotter
from EarthquakeSignal.tools.fourier_plotter import FourierPlotter
from EarthquakeSignal.tools.newmark_plotter import NewmarkPlotter
from EarthquakeSignal.tools.rotd_plotter import RotDPlotter

from EarthquakeSignal.tools.export_writer import ExportWriter

class EarthquakeSignal:
    """
    Represents a single processed earthquake record with its seismic signals and analysis options.
    """

    def __init__(self, filepath, config):
        self.filepath = filepath
        self.config = config
        self.name = None
        self.dt = None
        self.signals = {}            # H1, H2, V
        self.component_names = {}    # Map: H1 -> filename
        self.corrected_acc = {}
        self.corrected_vel = {}
        self.corrected_disp = {}
        self.arias = {}
        self.newmark_spectra = {}
        self.rotd = {}
        self.fourier = {}

        # Tools
        self.summary_tool = EarthquakeSummary(self)
        self.plotter_tool = EarthquakePlotter(self)
        self.comparison_tool = EarthquakeComparisonPlotter(self)
        self.arias_plotter = AriasPlotter(self)
        self.fourier_plotter = FourierPlotter(self)
        self.newmark_plotter = NewmarkPlotter(self)
        self.rotd_plotter = RotDPlotter(self)
        self.exporter = ExportWriter(self)

    def load_and_process(self):
        self._load_signal()
        self._identify_components()

        if self.config.get('apply_baseline_correction', False):
            self._apply_baseline_correction()
        if self.config.get('apply_arias_analysis', False):
            self._compute_arias_intensity()
        if self.config.get('apply_fourier_analysis', False):
            self._compute_fourier_analysis()
        if self.config.get('_compute_newmark_spectra', False):
            self._compute_newmark_spectra()
        if self.config.get('compute_rotd', False):
            self._compute_rotd()
        if self.config.get('print_summary', False):
            self.print_summary()
        if self.config.get('plot_signals', False):
            self.plot_original_signals()
        if self.config.get('plot_corrected_signals', False):
            self.plot_corrected_signals()
        if self.config.get('plot_arias_signals', False):
            self.plot_arias_signals()
        if self.config.get('plot_fourier_signals', False):
            self.plot_fourier_signals()
        if self.config.get('plot_newmark_spectra', False):
            self.plot_newmark_spectra()
        if self.config.get('plot_rotd', False):
            self.plot_rotd()
        if self.config.get('writer', False):
            self.export()

    def _load_signal(self):
        print('-- start load_signal-->Done!')
        loader = SignalLoader(self.filepath, self.config['file_extension'])
        self.dt, self.signals_raw = loader.read()
        unit_factor = self.config['unit_factor']
        self.signals_raw = {k: v / unit_factor for k, v in self.signals_raw.items()}

    def _identify_components(self):
        print('-- start identify components-->Done!')
        self.signals, self.component_names = SignalComponentIdentifier.identify(self.signals_raw)

    def _apply_baseline_correction(self):
        print('-- start apply base line-->Done!')
        for comp, signal in self.signals.items():
            acc_corr, vel_corr, disp_corr = BaselineCorrection.apply(signal, self.dt)
            self.corrected_acc[comp] = acc_corr
            self.corrected_vel[comp] = vel_corr
            self.corrected_disp[comp] = disp_corr

    def _compute_arias_intensity(self):
        print('-- start compute arias intensity-->Done!')
        self.arias = {}
        for comp, signal in self.signals.items():
            IA, t0, t1, ia_total, pot_dest = AriasIntensityAnalyzer.compute(signal, self.dt)
            self.arias[comp] = {
                'IA_percent': IA,
                't_start': t0,
                't_end': t1,
                'IA_total': ia_total,
                'pot_dest': pot_dest
            }

    def _compute_fourier_analysis(self):
        print('-- start compute fourier analysis-->Done!')
        self.fourier = {}
        for comp, signal in self.signals.items():
            f, Pyy, dom_freqs, dom_periods, dom_peaks = FourierAnalyzer.compute(signal, self.dt)
            self.fourier[comp] = {
                'frequencies': f,
                'spectrum': Pyy,
                'dominant_freqs': dom_freqs,
                'dominant_periods': dom_periods,
                'dominant_peaks': dom_peaks
            }

    def _compute_newmark_spectra(self):
        print('-- start compute newmark spectra->OK')
        self.newmark_spectra = {}
        for comp, acc in self.signals.items():
            spec = None
            spec_corr = NewmarkSpectrumAnalyzer.compute(self.corrected_acc[comp], self.dt)
            self.newmark_spectra[comp] = {
                'T': spec['T'] if spec else spec_corr['T'],
                'Sa': spec['Sa'] if spec else spec_corr['Sa'],
                'Sv': spec['Sv'] if spec else spec_corr['Sv'],
                'Sd': spec['Sd'] if spec else spec_corr['Sd'],
                'PSa': spec['PSa'] if spec else spec_corr['PSa'],
                'PSv': spec['PSv'] if spec else spec_corr['PSv'],
                'Sa_corr': spec_corr['Sa'],
                'Sv_corr': spec_corr['Sv'],
                'Sd_corr': spec_corr['Sd'],
                'PSa_corr': spec_corr['PSa'],
                'PSv_corr': spec_corr['PSv'],
                'u': spec['u'] if spec else spec_corr['u'],
                'v': spec['v'] if spec else spec_corr['v'],
                'a': spec['a'] if spec else spec_corr['a'],
                'at': spec['at'] if spec else spec_corr['at'],
                'u_corr': spec_corr['u'], 'v_corr': spec_corr['v'],
                'a_corr': spec_corr['a'], 'at_corr': spec_corr['at']
            }

    def _compute_rotd(self):
        print('-- start compute rotd-->Done!')
        h1 = self.corrected_acc['H1']
        h2 = self.corrected_acc['H2']
        self.rotd = RotDSpectrumAnalyzer.compute_rotd(h1, h2, self.dt)

    def print_summary(self):
        self.summary_tool.print_summary()

    def plot_original_signals(self, save_svg=True):
        self.plotter_tool.plot_original_signals(save_svg=save_svg)

    def plot_corrected_signals(self, save_svg=True):
        self.comparison_tool.plot_corrected_signals(save_svg=save_svg)

    def plot_arias_signals(self, save_svg=True):
        self.arias_plotter.plot_arias(save_svg=save_svg)

    def plot_fourier_signals(self, save_svg=True):
        self.fourier_plotter.plot_spectrum(save_svg=save_svg)

    def plot_newmark_spectra(self, save_svg=True):
        self.newmark_plotter.plot_newmark_spectra(save_svg=save_svg)

    def plot_rotd(self, save_svg=True):
        self.rotd_plotter.plot_rotd(save_svg=save_svg)

    def export(self, uncorrected=True, corrected=False, newmark_corrected=False):
        self.exporter.export( uncorrected=uncorrected, corrected=corrected, newmark_corrected=newmark_corrected  )
