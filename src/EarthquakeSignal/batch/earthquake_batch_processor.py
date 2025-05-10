"""
Description:
    This module defines the EarthquakeBatchProcessor class, which scans a folder of seismic signal
    files (.AT2, .TXT, etc.), groups them by RSN identifier or fallback to filename prefix, and 
    instantiates EarthquakeSignal objects for each group. It supports batch processing of both 
    NGA-West2 and custom-named records, ensuring each temporary folder reflects the identifier.

Date:
    2025-05-10
"""

__author__ = "Ing. Patricio Palacios B., M.Sc."
__version__ = "1.1.0"

import os
import shutil
import re
from EarthquakeSignal.models.earthquake_signal import EarthquakeSignal


class EarthquakeBatchProcessor:
    """
    Processes multiple earthquake records grouped by RSN or filename prefix in a target folder.
    """

    def __init__(self, folder_path, config):
        """
        Parameters
        ----------
        folder_path : str
            Path to the directory containing .AT2 or .TXT files.
        config : dict
            Configuration dictionary used to control each EarthquakeSignal instance.
        """
        self.folder_path = folder_path
        self.config = config
        self.earthquakes = {}

    def process_all(self):
        """
        Process all groups found in the input folder.

        Returns
        -------
        dict
            Dictionary of EarthquakeSignal instances keyed by RSN or prefix.
        """
        grouped_files = self._group_by_identifier()
        for group_id, filelist in grouped_files.items():
            self._process_group(group_id, filelist)
        return self.earthquakes

    def _group_by_identifier(self):
        """
        Groups files by RSN (e.g., RSN123) or fallback to prefix before first underscore.

        Returns
        -------
        dict
            Dictionary of grouped files by identifier.
        """
        ext = self.config.get("file_extension", ".AT2").upper()
        files = [f for f in os.listdir(self.folder_path) if f.upper().endswith(ext)]
        groups = {}

        for file in files:
            upper_file = file.upper()
            match = re.search(r'(RSN\d+)', upper_file)
            if match:
                group_id = match.group(1)
            elif "_" in file:
                group_id = file.split("_")[0]
            else:
                group_id = os.path.splitext(file)[0]  # Use entire filename if no underscores

            groups.setdefault(group_id, []).append(file)

        return groups

    def _process_group(self, group_id, filelist):
        """
        Process a group by creating a named folder and instantiating EarthquakeSignal.

        Parameters
        ----------
        group_id : str
            Identifier (RSN or filename prefix).
        filelist : list of str
            List of filenames in this group.
        """
        temp_dir = os.path.join(self.folder_path, group_id)
        os.makedirs(temp_dir, exist_ok=True)

        try:
            for file in filelist:
                shutil.copy(os.path.join(self.folder_path, file), temp_dir)

            eq = EarthquakeSignal(temp_dir, self.config)
            eq.load_and_process()
            self.earthquakes[group_id] = eq

        finally:
            shutil.rmtree(temp_dir)

    def export_to_globals(self):
        """
        Optionally push each processed EarthquakeSignal to the global namespace using its ID.
        """
        for group_id, obj in self.earthquakes.items():
            globals()[group_id] = obj
