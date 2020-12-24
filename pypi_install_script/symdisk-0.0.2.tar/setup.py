from setuptools import setup, find_packages
from pathlib import Path
import os

here = Path(__file__).parent.absolute()
project_name = 'symdisk'

setup(
    name = project_name,
    version        = __import__(project_name).__version__,
    author         = __import__(project_name).__author__,
    author_email   = __import__(project_name).__contact__,
    url = 'https://gitlab.oca.eu/crobert/symdisk-project',
    description = 'Disk modelling with sympy',
    license = 'GNU',
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.6'
    ],
    keywords = 'math modelling protoplanetary-disks',
    install_requires = ['sympy>=1.1.1'],
    python_requires = '>=3.6',
    packages = find_packages(),
)
