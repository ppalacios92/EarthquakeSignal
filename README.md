# EarthquakeSignal

A Python-based framework for processing earthquake ground-motion records at scale. The package automates baseline correction, frequency-domain filtering, Fourier analysis, Arias intensity, and response spectra (including RotD) for the three components of each record, with batch/parallel workflows for local machines.

---

## ⚙️ Features

- Modular processing pipeline for ground-motion signals (H1, H2, V).
- Baseline correction and drift removal.
- Frequency filtering and spectral analysis (FFT).
- Arias Intensity computation and visualization.
- Response spectra via Newmark method (PSa/PSv/Pd as configured).
- Rotation-independent spectra (RotD00/50/100).
- Batch processing for large sets of records (parallel-ready).
- Clear plotting utilities for QA/QC and publication-ready figures.
- Examples notebook to showcase end-to-end usage.

_Core capabilities are implemented under `src/EarthquakeSignal/core/` (e.g., `base_line.py`, `fourier_analyzer.py`, `newmark_spectrum_analyzer.py`, `rotd_analyzer.py`, `arias_intensity.py`) with dedicated plotters under `src/EarthquakeSignal/tools/` and batch utilities under `src/EarthquakeSignal/batch/`. An example notebook lives in `src/EarthquakeSignal/examples/`._

**Supported input formats**
- Plain text formats commonly used for ground motions, including **`.AT2`** (PEER) and **`.TXT`** (per recent updates).

---

## 📦 Requirements

- **Windows, macOS, or Linux**
- **Python 3.9+** (recommended)
- Python libraries:
  - `numpy`, `pandas`, `scipy`, `matplotlib`
  - `numba` (optional, for speedups)
  - Standard library `multiprocessing` (for batch/parallel runs)

> Note: If you plan to run the example notebook, ensure Jupyter is available in your environment. The repo already contains an example under `src/EarthquakeSignal/examples/`.

---

## 🚀 Installation

Clone and install in editable mode:

```bash
git clone https://github.com/ppalacios92/EarthquakeSignal.git
cd EarthquakeSignal
pip install -e .
```


---

## 📁 Repository Structure
```bash
EarthquakeSignal/
├── README.md
├── setup.py
├── src/
│   └── EarthquakeSignal/
│       ├── batch/
│       │   └── earthquake_batch_processor.py
│       ├── config/
│       │   └── settings.py
│       ├── core/
│       │   ├── arias_intensity.py
│       │   ├── base_line.py
│       │   ├── fourier_analyzer.py
│       │   ├── newmark_spectrum_analyzer.py
│       │   ├── rotd_analyzer.py
│       │   ├── signal_components.py
│       │   └── signal_loader.py
│       ├── examples/
│       │   ├── Example.ipynb
│       │   └── data/
│       ├── models/
│       │   └── earthquake_signal.py
│       └── tools/
│           ├── arias_plotter.py
│           ├── earthquake_comparison_plotter.py
│           ├── earthquake_plotter.py
│           ├── earthquake_summary.py
│           ├── fourier_plotter.py
│           ├── newmark_plotter.py
│           └── rotd_plotter.py
└── EarthquakeSignal.egg-info/

```

---
## 🛑 Disclaimer
This tool is provided as-is, without any guarantees of accuracy, performance, or suitability for specific engineering tasks. The author assumes no responsibility for the interpretation of results, post-processing errors, or consequences of incorrect data handling.
Use at your own risk and validate outcomes against authoritative references, original records, and relevant codes.

---
## 👨‍💻 Author

Developed by Patricio Palacios B.
Structural Engineer | Python Developer | Seismic Modeler
GitHub: @ppalacios92

## 📚 How to Cite

If you use this tool in your work, please cite it as follows:

```bibtex
@misc{palacios2025earthquakesignal,
  author       = {Patricio Palacios B.},
  title        = {EarthquakeSignal: A modular framework for earthquake ground-motion processing},
  year         = {2025},
  publisher    = {GitHub},
  journal      = {GitHub repository},
  howpublished = {\url{https://github.com/ppalacios92/EarthquakeSignal}}
}
```

## 📄 Citation in APA (7th Edition)

Palacios B., P. (2025). EarthquakeSignal: A modular framework for earthquake ground-motion processing [Computer software]. GitHub. https://github.com/ppalacios92/EarthquakeSignal
