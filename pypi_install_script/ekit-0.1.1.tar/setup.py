#!/usr/bin/env python

import os
import sys

from setuptools import find_packages, setup

requirements = ["pyyaml", "numpy"]

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read().replace(".. :changelog", "")


doclink = """
Documentation
-------------

A selection of small everyday tools.

At the moment includes a context handler, logging tool and a tool to standardize paths.

Please visit the Project Homepage: http://cosmo-docs.phys.ethz.ch/ekit for the Documenta      tion."""

PACKAGE_PATH = os.path.abspath(os.path.join(__file__, os.pardir))

setup(
    name="ekit",
    version="0.1.1",
    description="Selection of small, general tools",
    long_description=doclink,
    author="Dominik Zuercher",
    author_email="dominikz@phys.ethz.ch",
    url="https://cosmo-docs.phys.ethz.ch/ekit",
    packages=find_packages(include=["ekit"]),
    include_package_data=True,
    install_requires=requirements,
    license="MIT License",
    zip_safe=False,
    keywords="ekit",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.7",
    ],
)
