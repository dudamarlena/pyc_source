#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright © 2020 Aleksandr Suvorov
# Licensed under the terms of the MIT License
# (see LICENSE.txt for details)
# -----------------------------------------------------------------------------
# Aleksandr Suvorov (hackband)
# Yandex Money: https://money.yandex.ru/to/4100110928527458
# Sberbank Russia: 4276 4417 5763 7686
# PayPal: paypal.me/py2ru
# Email: smart-py@yandex.ru
# Github: https://github.com/hackband/scleaner
# Site: https://py2.ru
# PyPi: https://pypi.org/project/scleaner/
# -----------------------------------------------------------------------------
from setuptools import setup, find_packages
from os.path import join, dirname

PACKAGE = "scleaner"
VERSION = __import__(PACKAGE).__version__
AUTHOR = 'Aleksandr Suvorov'
AUTHOR_EMAIL = "smart-py@ya.ru"
DESCRIPTION = "Package for mashing, zeroing, and deleting files. Work with paths to files and folders." \
              "Aleksandr Suvorov | smart-py@ya.ru | Donate: 4276 4417 5763 7686"
NAME = "scleaner"
URL = "https://github.com/hackband/scleaner"
LICENSE = 'MIT'
LONG_DESCRIPTION = open(join(dirname(__file__), 'README.txt')).read()
INSTALL_REQUIRES = ['pyside2']
PLATFORM = ['Linux, Windows']
CLASSIFIERS = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]
KEYWORDS = [
    'scleaner',
    'shred files',
    'zero files',
    'del files',
    'py2.ru',
    'smartcleaner',
    'smart cleaner',
    'hackband'
]
setup(
    name=NAME,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    description=DESCRIPTION,
    version=VERSION,
    license=LICENSE,
    platforms=PLATFORM,
    packages=find_packages(),
    long_description=LONG_DESCRIPTION,
    install_requires=INSTALL_REQUIRES,
    include_package_data=True,
    zip_safe=False,
    keywords=KEYWORDS
)

