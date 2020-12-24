from setuptools import setup, find_packages
from pathlib import Path
import os

here = Path(__file__).parent.absolute()
project_name = 'amrvac_pywrap'

setup(
    name = project_name,
    version        = __import__(project_name).__version__,
    author         = __import__(project_name).__author__,
    author_email   = __import__(project_name).__contact__,
    url = 'https://gitlab.oca.eu/crobert/amrvac-pywrap-project',
    description = 'AMRVAC simulations as python objects',
    license = 'GNU',
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.6'
    ],
    keywords = 'wrapper',
    install_requires = [
        'f90nml>=1.0.2',
        'vtk_vacreader>=1.0.0'
    ],
    python_requires = '>=3.6',
    packages = find_packages(),
    #entry_points={'console_scripts': ['amrvac_convert=amrvac_convert:main']}
)
