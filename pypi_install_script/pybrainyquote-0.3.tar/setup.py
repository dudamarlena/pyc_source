#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup
import pathlib
 
 
NAME = "pybrainyquote"

DESCRIPTION = "Get quotes from brainyquote.com"
 
LONG_DESCRIPTION = pathlib.Path("README.txt").read_text()
 
KEYWORDS = "Brainyquote"
 
AUTHOR = "William Song"
 
AUTHOR_EMAIL = "songcwzjut@163.com"
 
URL = "https://github.com/Freakwill/%s" % NAME
 
VERSION = "0.3" # update the version before uploading
 
LICENSE = "MIT"

 
setup(
    name = NAME,
    py_modules= [NAME],
    version = VERSION,
    description = DESCRIPTION,
    long_description = LONG_DESCRIPTION,
    classifiers = [
        'License :: Public Domain',  # Public Domain
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Intended Audience :: Education',
        'Operating System :: OS Independent',
        'Topic :: Education',
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
