"""
Description:
    This module provides a class for identifying the horizontal and vertical components
    of a seismic signal based on filename suffix or RMS (Root Mean Square) energy.

    Priority is given to filename-based identification when filenames end with
    _X, _Y, or _Z (before extension), corresponding to components H1, H2, and V.
    If this fails, fallback to energy-based identification is used.
    If config['file_names_p'] and config['file_names_n'] are provided, those files
    are directly assigned to H1 and H2 (compared by base filename, case-insensitive).

Date:
    2025-06-10
"""

__author__ = "Ing. Patricio Palacios B., M.Sc."
__version__ = "1.3.2"

import numpy as np
import os


class SignalComponentIdentifier:
    """
    Identifies the V, H1, and H2 components in a set of 3 seismic signals.
    """

    @staticmethod
    def identify(signals: dict, config=None):
        """
        Identify the three seismic components: H1, H2, and V.

        Parameters
        ----------
        signals : dict
            Dictionary where keys are full paths or names and values are numpy arrays of the signals.
        config : dict or None
            Configuration dictionary. If provided and contains 'file_names_p' and 'file_names_n',
            these will be used as H1 and H2 respectively (compared by base filename, case-insensitive).

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

        # --- Opción explícita desde config ---
        if config and 'file_names_p' in config and 'file_names_n' in config:
            
            file_p_list = [f.upper() for f in config['file_names_p']]
            file_n_list = [f.upper() for f in config['file_names_n']]

            # Diccionario con claves en mayúsculas para comparación insensible a case
            signal_keys_by_basename = {
                os.path.basename(k).upper(): k for k in signals.keys()
            }

            match_p = None
            match_n = None

            for name_upper in signal_keys_by_basename:
                if name_upper in file_p_list:
                    match_p = signal_keys_by_basename[name_upper]
                elif name_upper in file_n_list:
                    match_n = signal_keys_by_basename[name_upper]

            if not match_p or not match_n:
                raise ValueError("Could not match 'file_names_p' or 'file_names_n' with loaded signal filenames.")

            identified['H1'] = signals[match_p]
            names['H1'] = os.path.splitext(os.path.basename(match_p))[0]
            identified['H2'] = signals[match_n]
            names['H2'] = os.path.splitext(os.path.basename(match_n))[0]

            # Detectar el que no está
            for k in signals:
                base = os.path.basename(k).upper()
                if base not in file_p_list and base not in file_n_list:
                    identified['V'] = signals[k]
                    names['V'] = os.path.splitext(os.path.basename(k))[0]
                    break

            if set(identified.keys()) != {'H1', 'H2', 'V'}:
                raise RuntimeError("Failed to assign all three components (H1, H2, V) using config.")
            return identified, names

        # --- Identificación por sufijo _X, _Y, _Z ---
        filename_map = {'_X': 'H1', '_Y': 'H2', '_Z': 'V'}
        for key in signals.keys():
            basename = os.path.splitext(os.path.basename(key))[0]
            for suffix, label in filename_map.items():
                if basename.upper().endswith(suffix):
                    if label in identified:
                        raise ValueError(f"Duplicate component label detected for {label}")
                    identified[label] = signals[key]
                    names[label] = basename
                    break

        # --- Fallback por RMS si falta alguna componente ---
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
                names[label] = os.path.splitext(os.path.basename(fname))[0]

        # --- Validación final ---
        if set(identified.keys()) != {'H1', 'H2', 'V'}:
            raise RuntimeError("Failed to assign all three components (H1, H2, V).")

        return identified, names
