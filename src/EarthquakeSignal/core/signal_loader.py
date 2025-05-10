"""
Description:
    This module contains the SignalLoader class which reads and processes seismic signal files
    from a given folder path. It supports .AT2, vertical TXT, and RENAC horizontal formats.
    The loader extracts the sampling interval from DT lines or computes it from frequency metadata.
    It parses data in horizontal or vertical format, pads signals to equal length,
    and fills malformed lines with zeros when needed.

Date:
    2025-05-10
"""

__author__ = "Ing. Patricio Palacios B., M.Sc."
__version__ = "1.2.1"

import os
import numpy as np
import re

class SignalLoader:
    """
    SignalLoader reads seismic signals from various formats and returns
    the sampling interval and aligned signal arrays.
    """

    def __init__(self, path, extension):
        """
        Initialize the SignalLoader with the folder path and file extension.

        Parameters
        ----------
        path : str
            Directory containing the signal files.
        extension : str
            Extension of the files to read (e.g., '.AT2', '.TXT').
        """
        self.path = path
        self.extension = extension.upper()

    def read(self):
        """
        Read and process seismic signal files in the given path.

        Returns
        -------
        dt : float
            Sampling interval [s].
        signals : dict
            Dictionary with filenames as keys and acceleration arrays as values.
        """
        files = [f for f in os.listdir(self.path) if f.upper().endswith(self.extension)]
        if not files:
            raise FileNotFoundError(f"No files with extension {self.extension} found in {self.path}")

        dt = None
        signals = {}

        for file in files:
            full_path = os.path.join(self.path, file)
            with open(full_path, 'r') as f:
                lines = f.readlines()

            current_dt = None
            data_lines = []
            data_str = ""

            # --- Caso 1: formato AT2 clásico con DT= ---
            dt_line = next((line for line in lines if 'DT=' in line.upper()), None)
            if dt_line:
                match = re.search(r'DT\s*=\s*([0-9.Ee+-]+)', dt_line)
                if not match:
                    raise ValueError(f"Invalid DT format in file {file}")
                current_dt = float(match.group(1))
                idx_start = lines.index(dt_line) + 1
                data_lines = lines[idx_start:]
                data_str = ' '.join(self._clean_lines(data_lines))

            # --- Caso 2: formato vertical con línea "DT = 0.005" ---
            elif any("DT" in l.upper() for l in lines):
                for i, line in enumerate(lines):
                    if "DT" in line.upper():
                        match = re.search(r'([0-9.Ee+-]+)', line)
                        current_dt = float(match.group(1))
                        idx_start = i + 1
                        data_lines = lines[idx_start:]
                        break
                data_str = '\n'.join([line.strip() for line in data_lines if line.strip()])

            # --- Caso 3: formato RENAC con frecuencia de muestreo ---
            elif any("FRECUENCIA" in l.upper() and "HZ" in l.upper() for l in lines):
                freq_line = next(line for line in lines if "FRECUENCIA" in line.upper())
                match = re.search(r'([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)', freq_line)
                if not match:
                    raise ValueError(f"No numeric frequency found in line: {freq_line}")
                frequency = float(match.group(1))
                current_dt = 1.0 / frequency

                # Buscar línea separadora para comenzar datos
                separator_index = next(i for i, l in enumerate(lines) if set(l.strip()) == set("_"))
                data_lines = lines[separator_index + 1:]
                clean_lines = [line.strip() for line in data_lines if line.strip()]
                data_str = ' '.join(clean_lines)

            else:
                raise ValueError(f"Unsupported file format in file: {file}")

            # Validar consistencia de dt
            if dt is None:
                dt = current_dt
            elif abs(current_dt - dt) > 1e-6:
                raise ValueError(f"Inconsistent sampling interval in file {file}: {current_dt} ≠ {dt}")

            # Convertir a arreglo NumPy
            data_values = np.fromstring(data_str, sep=' ')
            signals[file] = data_values

        # Padding para igualar longitudes
        max_len = max(len(sig) for sig in signals.values())
        for fname, sig in signals.items():
            if len(sig) < max_len:
                padding = np.zeros(max_len - len(sig))
                signals[fname] = np.concatenate([sig, padding])
                print(f"[WARNING] Signal '{fname}' was padded with zeros to reach {max_len} samples.")

        return dt, signals

    def _clean_lines(self, data_lines):
        """
        Process data lines and fill invalid lines with zeros.

        Parameters
        ----------
        data_lines : list of str
            Raw lines after DT metadata line.

        Returns
        -------
        list of str
            Cleaned lines containing only valid numeric data.
        """
        clean_lines = []
        for line in data_lines:
            try:
                _ = [float(v) for v in line.strip().split()]
                clean_lines.append(line.strip())
            except ValueError:
                if clean_lines:
                    avg_len = int(np.mean([len(l.split()) for l in clean_lines]))
                    zero_line = ' '.join(['0.0'] * avg_len)
                    clean_lines.append(zero_line)
                else:
                    clean_lines.append('0.0')
        return clean_lines
