from setuptools import setup, find_packages

setup(
    name="EarthquakeSignal",
    version="1.0.0",
    author="Ing. Patricio Palacios B., M.Sc.",
    description="A modular framework for processing earthquake ground motion signals.",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    python_requires=">=3.7",
)
