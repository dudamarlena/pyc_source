# -*- coding: iso-8859-1 -*-
from distutils.core import setup#,find_packages

setup(
    name = 'EMMSA',
    packages = ['EMMSA','docs'],
    version = '0.0.4',
    description = 'Multivariate Statistical Analysis for Electron Microscopy Data',
    author = 'Michael Sarahan',
    author_email = 'msarahan@gmail.com',
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Other Environment",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Scientific/Engineering :: Chemistry",
        "Topic :: Scientific/Engineering :: Physics",
        ],
    install_requires=[
        "rpy2>=2.1",
        "pandas>=0.3",
	"elixir",
        ],
    package_data = {
	'EMMSA':['utils/*.py','utils/templates/*.footer'],
	'docs':['docs/*']
	}
    )

