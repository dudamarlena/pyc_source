#!/usr/bin/env python3
 
from setuptools import setup
import pathlib
 
 
NAME = "zhfnote"

DESCRIPTION = "A tool for learning English"
 
LONG_DESCRIPTION = pathlib.Path("README.txt").read_text()
 
KEYWORDS = "English Learning"
 
AUTHOR = "Huanfeng Zheng"
 
AUTHOR_EMAIL = "www.670267038@qq.com"
 
URL = "https://github.com/Freakwill"
 
VERSION = "0.4" # update the version before uploading
 
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
        'Programming Language :: Python :: 3.6',
        'Operating System :: OS Independent',
        'Topic :: Education',
        'Natural Language :: English'
    ],
    keywords = KEYWORDS,
    author = AUTHOR,
    author_email = AUTHOR_EMAIL,
    # url = URL,
    license = LICENSE,
    # packages = PACKAGES,
    include_package_data=True,
    zip_safe=True,
)
