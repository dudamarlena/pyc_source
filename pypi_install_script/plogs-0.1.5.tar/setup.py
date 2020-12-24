# -*- coding: utf8 -*-

# File: setup.py
# Author: Doug Rudolph
# Created: November 19, 2018


import setuptools

# copies README into `long_description`
with open('README.md', 'r') as readme:
    long_description = readme.read()


setuptools.setup(

    # general metadata
    name="plogs",
    version="0.1.5",
    author="Doug Rudolph",
    author_email="drudolph914@gmail.com",

    # shorthand description
    description="Bring color and formatting to your logs",

    # copies the README.md into `long_description` and notes that it is a markdown file
    long_description=long_description,
    long_description_content_type="text/markdown",

    # GitHub URL
    url="https://github.com/11/plogs",

    # when downloading plogs, the user only needs access to the src/ directory
    packages=["plogs"],
    package_dir={"plogs": "src"},

    # specify what version of python plogs is targeting
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
