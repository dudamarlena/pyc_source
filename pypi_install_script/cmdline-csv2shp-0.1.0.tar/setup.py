# -*- coding: utf-8 -*-
 
"""setup.py: setuptools control."""

import re
import os
from setuptools import setup, find_packages
 
#os.system("pip install -r requirents.txt")
version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('csv2shp/csv2shp.py').read(),
    re.M
    ).group(1)
 

with open("README.md", "rb") as f:
    long_descr = f.read().decode("utf-8")

#with open('requirements.txt') as f:
#    required = f.read().splitlines()
 
setup(
    name = "cmdline-csv2shp",
    packages = ["csv2shp"],
    entry_points = {
        "console_scripts": ['csv2shp = csv2shp.csv2shp:main']
        },
    version = version,
    description = "Python command line application for converting csv to shapefile.",
    long_description = long_descr,
    author = "Abdulvahab Kharadi",
    author_email = "a.kharadi@hrwallingford.com",
    url = "https://hrwallingford.com",
   
    package_data={},
    #install_requires=required,
    include_package_data=True,
    )