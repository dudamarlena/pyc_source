# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 23:21:46 2020

@author: Anurag Agarwal
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 19:49:25 2020
@author: AVANI AGARWAL 101703122
"""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="topsis_avani", # Replace with your own username
    version="0.0.1",
    author="avani/avaniagarwal",
    author_email="avaniagarwal1999@gmail.com",
    description="Implementation of topsis over a csv datafile using the distance calculation and comparison approach",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Avani-Agarwal1999/Topsis_Avani_3122.git",
    download_url="https://github.com/Avani-Agarwal1999/Topsis_Avani_3122/archive/0.0.1.tar.gz",
    packages=["topsis_avani"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
