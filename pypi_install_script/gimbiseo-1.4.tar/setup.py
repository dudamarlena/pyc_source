# -*- coding: utf-8 -*-

import pathlib

#try:
from setuptools import setup
#except:
#    from distutils.core import setup


NAME = "gimbiseo"

PACKAGES = ["gimbiseo",]

DESCRIPTION = "A system of Human-Machine Dialogue"

LONG_DESCRIPTION = "See homepage"

KEYWORDS = "owlready DLs OWL inference"

AUTHOR = "William Song"

AUTHOR_EMAIL = "songcwzjut@163.com"

URL = "https://git.oschina.net/williamzjc/gimbiseo"

VERSION = "1.4"

LICENSE = "MIT"


setup(
    name = NAME,
    version = VERSION,
    description = DESCRIPTION,
    long_description = LONG_DESCRIPTION,
    classifiers = [
        'License :: Public Domain',  # Public Domain
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Intended Audience :: Science/Research',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Natural Language :: English'
    ],
    keywords = KEYWORDS,
    author = AUTHOR,
    author_email = AUTHOR_EMAIL,
    url = URL,
    license = LICENSE,
    packages = PACKAGES,
    include_package_data=True,
    zip_safe=True,
)