"""
Description:
    This module defines the EarthquakeBatchProcessor class, which scans a folder of seismic signal
    files, groups them by RSN identifier, and instantiates EarthquakeSignal objects for each set.
    It supports batch processing of multiple earthquake records in a clean and modular way.

Date:
    2025-05-01
"""

__author__ = "Ing. Patricio Palacios B., M.Sc."
__version__ = "1.0.0"

import os
import shutil
import re
from EarthquakeSignal.models.earthquake_signal import EarthquakeSignal


class EarthquakeBatchProcessor:
    """
    Processes multiple earthquake records grouped by RSN prefix in a target folder.
    """

    def __init__(self, folder_path, config):
        """
        Parameters
        ----------
        folder_path : str
            Path to the directory containing .AT2 files.
        config : dict
            Configuration dictionary used to control each EarthquakeSignal instance.
        """
        self.folder_path = folder_path
        self.config = config
        self.earthquakes = {}

    def process_all(self):
        """
        Process all RSN groups found in the input folder.

        Returns
        -------
        dict
            Dictionary of EarthquakeSignal instances keyed by RSN ID.
        """
        rsn_groups = self._group_by_rsn()
        for rsn, filelist in rsn_groups.items():
            self._process_rsn_group(rsn, filelist)
        return self.earthquakes

    def _group_by_rsn(self):
        """
        Groups filenames based on the RSN identifier (e.g., RSN123).

        Returns
        -------
        dict
            Dictionary where keys are RSN identifiers and values are lists of filenames.
        """
        files = [f for f in os.listdir(self.folder_path) if f.upper().endswith('.AT2')]
        rsn_groups = {}

        for file in files:
            match = re.search(r'(RSN\d+)', file.upper())
            if match:
                rsn = match.group(1)
                rsn_groups.setdefault(rsn, []).append(file)
            else:
                print(f"[WARNING] No RSN identifier found in file: {file}")

        return rsn_groups

    def _process_rsn_group(self, rsn, filelist):
        """
        Processes a single RSN group by creating a temporary folder and instantiating EarthquakeSignal.

        Parameters
        ----------
        rsn : str
            The RSN identifier (e.g., 'RSN123').
        filelist : list of str
            List of filenames belonging to this RSN.
        """
        temp_dir = os.path.join(self.folder_path, f'_temp_{rsn}')
        os.makedirs(temp_dir, exist_ok=True)

        for file in filelist:
            shutil.copy(os.path.join(self.folder_path, file), temp_dir)

        eq = EarthquakeSignal(temp_dir, self.config)
        eq.load_and_process()
        self.earthquakes[rsn] = eq

        shutil.rmtree(temp_dir)

    def export_to_globals(self):
        """
        Optionally push each processed EarthquakeSignal to the global namespace using its RSN ID.
        """
        for rsn, obj in self.earthquakes.items():
            globals()[rsn] = obj
