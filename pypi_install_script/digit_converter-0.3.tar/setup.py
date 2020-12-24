#!/usr/bin/env python3
 
from setuptools import setup
import pathlib
 

NAME = "digit_converter"

DESCRIPTION = "A cool tool for digits converting. It could be applied in GA."
 
LONG_DESCRIPTION = pathlib.Path("README.txt").read_text()
 
KEYWORDS = "Digit Converting, GA"
 
AUTHOR = "William Song"
 
AUTHOR_EMAIL = "songcwzjut@163.com"
 
URL = f"https://github.com/Freakwill/{NAME}"
 
VERSION = "0.3" # update the version before uploading

LICENSE = "MIT"

 
setup(
    name = NAME,
    py_modules = [NAME],
    version = VERSION,
    description = DESCRIPTION,
    long_description = LONG_DESCRIPTION,
    classifiers = [
        'License :: Public Domain',  # Public Domain
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Intended Audience :: Science/Research',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Natural Language :: English'
    ],
    keywords = KEYWORDS,
    author = AUTHOR,
    author_email = AUTHOR_EMAIL,
    url = URL,
    license = LICENSE,
    # packages = PACKAGES,
    include_package_data=True,
    zip_safe=True,
)
