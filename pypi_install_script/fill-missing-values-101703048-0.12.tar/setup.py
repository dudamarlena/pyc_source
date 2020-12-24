# -*- coding: utf-8 -*-
"""
Created on Sun Feb 16 

@author: akriti
"""
#Made by AkritiSehgal(101703048)
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fill-missing-values-101703048",
    version="0.12",
    author="Akriti Sehgal",
    author_email="akritisehgal9@gmail.com",
    description="A small package for filling missing values in the given dataset",
    long_description=long_description,
    long_description_content_type="text/markdown",
    download_url="https://github.com/AkritiSehgal/fill-missing-values-101703048/archive/v_01.2.tar.gz",
    keywords = ['command-line', 'Missing values', 'missing-values'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)
