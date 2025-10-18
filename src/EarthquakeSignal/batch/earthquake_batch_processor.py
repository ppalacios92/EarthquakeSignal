"""
Description:
    This module defines the EarthquakeBatchProcessor class, which scans a folder of seismic signal
    files (.AT2, .TXT, etc.), groups them by RSN identifier or fallback to filename prefix, and 
    instantiates EarthquakeSignal objects for each group. It supports batch processing of both 
    NGA-West2 and custom-named records, including two-column formats where dt is implicit from time
    and acceleration is in the second column.

Date:
    2025-06-10
"""

__author__ = "Ing. Patricio Palacios B., M.Sc."
__version__ = "1.4.0"

import os
import shutil
import re
import tempfile
from tqdm import tqdm
from joblib import Parallel, delayed

from EarthquakeSignal.models.earthquake_signal import EarthquakeSignal


class EarthquakeBatchProcessor:
    """
    Processes multiple earthquake records grouped by RSN or filename prefix in a target folder.
    """

    def __init__(self, folder_path, config, n_jobs=4):
        """
        Parameters
        ----------
        folder_path : str
            Path to the directory containing .AT2 or .TXT files.
        config : dict
            Configuration dictionary used to control each EarthquakeSignal instance.
        n_jobs : int
            Number of parallel processes to use.
        """
        self.folder_path = folder_path
        self.config = config
        self.n_jobs = n_jobs
        self.earthquakes = {}

    def process_all(self):
        """
        Process all groups found in the input folder using parallel processes.

        Returns
        -------
        dict
            Dictionary of EarthquakeSignal instances keyed by RSN or prefix.
        """
        grouped_files = list(self._group_by_identifier().items())

        def process_one_group(group_id, filelist):
            return group_id, self._process_group(group_id, filelist)

        results = Parallel(n_jobs=self.n_jobs, prefer="processes")(
            delayed(process_one_group)(group_id, filelist)
            for group_id, filelist in tqdm(grouped_files, desc="Processing earthquakes")
        )

        for group_id, eq in results:
            self.earthquakes[group_id] = eq

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
                group_id = os.path.splitext(file)[0]

            groups.setdefault(group_id, []).append(file)

        return {k: v for k, v in groups.items() if len(v) == 3}

    def _process_group(self, group_id, filelist):
        """
        Process a group by creating a temp folder and instantiating EarthquakeSignal.

        Parameters
        ----------
        group_id : str
            Identifier (RSN or filename prefix).
        filelist : list of str
            List of filenames in this group.

        Returns
        -------
        EarthquakeSignal
            Processed object instance.
        """
        temp_dir = tempfile.mkdtemp()
        try:
            for file in filelist:
                src_path = os.path.join(self.folder_path, file)
                dst_path = os.path.join(temp_dir, file)

                with open(src_path, 'r') as f:
                    lines = [line.strip() for line in f if line.strip()]
                    if len(lines) >= 2 and len(lines[0].split()) == 2:
                        time1, _ = map(float, lines[0].split())
                        time2, _ = map(float, lines[1].split())
                        dt = time2 - time1
                        acc = [line.split()[1] for line in lines]
                        with open(dst_path, 'w') as out:
                            out.write(f"NPTS={len(acc)}, DT={dt:.6f}\n")
                            for a in acc:
                                out.write(f"{a}\n")
                    else:
                        shutil.copy(src_path, dst_path)

            eq = EarthquakeSignal(temp_dir, self.config)
            eq.name = group_id
            eq.load_and_process()
            return eq

        finally:
            shutil.rmtree(temp_dir)

    def export_to_globals(self):
        """
        Optionally push each processed EarthquakeSignal to the global namespace using its ID.
        """
        for group_id, obj in self.earthquakes.items():
            globals()[group_id] = obj
