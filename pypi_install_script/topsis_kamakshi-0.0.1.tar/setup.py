# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 19:49:25 2020
@author: kamakshi_behl
"""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="topsis_kamakshi", # Replace with your own username
    version="0.0.1",
    author="kamakshi/kamakshi_behl",
    author_email="kamakshi.behl22@gmail.com",
    description="Implementation of topsis over a csv datafile using the distance calculation and comparison approach",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kamakshibehl/topsis_kamakshi.git",
    download_url="https://github.com/kamakshibehl/topsis_kamakshi/archive/0.0.1.tar.gz",
    packages=["topsis_kamakshi"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)