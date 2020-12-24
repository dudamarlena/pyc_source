# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 19:49:25 2020

@author: ashwin_menon
"""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="topsis_ashwin", # Replace with your own username
    version="0.0.3",
    author="ashwin_menon",
    author_email="ashwin.s.menon1999@gmail.com",
    description="Implementation of topsis over a csv datafile using the distance calculation and comparison approach",
    long_description="",
    long_description_content_type="text/markdown",
    url="https://github.com/ash-1999/topsis_ashwin",
    download_url="https://github.com/ash_1999/topsis_ashwin/archive/0.0.3.tar.gz",
    packages=["topsis_ashwin"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)