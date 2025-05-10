"""
Description:
    This module contains the SignalLoader class which reads and processes seismic signal files
    from a given folder path. It supports reading .AT2 files, extracting sampling interval (dt),
    and parsing acceleration values. It also handles missing or inconsistent lines and fills
    them with zeros, ensuring all signals are padded to the same length.

Date:
    2025-05-01
"""

__author__ = "Ing. Patricio Palacios B., M.Sc."
__version__ = "1.0.0"

import os
import numpy as np
import re

class SignalLoader:
    def __init__(self, path, extension='.AT2'):
        self.path = path
        self.extension = extension

    def read(self):
        files = [f for f in os.listdir(self.path) if f.upper().endswith(self.extension.upper())]
        if not files:
            raise FileNotFoundError(f"No files with extension {self.extension} found in {self.path}")

        dt = None
        signals = {}

        for file in files:
            full_path = os.path.join(self.path, file)
            with open(full_path, 'r') as f:
                lines = f.readlines()

            dt_line = next((line for line in lines if 'DT=' in line.upper()), None)
            if dt_line is None:
                raise ValueError(f"No DT line found in file {file}")

            match = re.search(r'DT\s*=\s*([0-9.Ee+-]+)', dt_line)
            current_dt = float(match.group(1))
            if dt is None:
                dt = current_dt
            elif abs(current_dt - dt) > 1e-6:
                raise ValueError(f"Inconsistent sampling interval in file {file}: {current_dt} ≠ {dt}")

            idx_start = lines.index(dt_line) + 1
            data_lines = lines[idx_start:]
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

            data_str = ' '.join(clean_lines)
            data_values = np.fromstring(data_str, sep=' ')
            signals[file] = data_values

        max_len = max(len(sig) for sig in signals.values())
        for fname, sig in signals.items():
            if len(sig) < max_len:
                padding = np.zeros(max_len - len(sig))
                signals[fname] = np.concatenate([sig, padding])
                print(f"[WARNING] Signal '{fname}' was padded with zeros to reach {max_len} samples.")

        return dt, signals
