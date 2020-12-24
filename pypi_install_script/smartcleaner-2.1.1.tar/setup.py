#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright © 2020 Aleksandr Suvorov
# Licensed under the terms of the MIT License
# (see LICENSE.txt for details)
# -----------------------------------------------------------------------------
# Aleksandr Suvorov (CyberLegioner)
# Github: https://github.com/CyberLegioner/smartcleaner
# Donate: https://money.yandex.ru/to/4100110928527458
# Site: https://py2.ru
# Email: smart-py@yandex.ru
# PyPi: https://pypi.org/project/smartcleaner/
# -----------------------------------------------------------------------------
from setuptools import setup, find_packages
from os.path import join, dirname

PACKAGE = "smartcleaner"
VERSION = __import__(PACKAGE).__version__
AUTHOR = 'Aleksandr Suvorov'
AUTHOR_EMAIL = "smart-py@ya.ru"
DESCRIPTION = "Program for overwriting, deleting, zeroing files."
NAME = "smartcleaner"
URL = "https://github.com/CyberLegioner/smartcleaner"
LICENSE = 'MIT'
PLATFORM = ['Linux, Windows']
LONG_DESCRIPTION = open(join(dirname(__file__), 'README.txt')).read()
INSTALL_REQUIRES = ['pyside2', 'scleaner']
CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: X11 Applications :: Qt',
    'License :: OSI Approved :: MIT License',
    'Operating System :: Microsoft :: Windows',
    'Operating System :: POSIX :: Linux',
    'Programming Language :: Python :: 3.7',
]
ENTRY_POINTS = {
    'gui_scripts':
        ['smartcleaner = smartcleaner.smart_cleaner:main']
}
KEYWORDS = [
    'smartcleaner',
    'shred files',
    'zero files',
    'del files',
    'py2.ru',
    'smart cleaner',
    'scleaner',
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
    entry_points=ENTRY_POINTS,
    install_requires=INSTALL_REQUIRES,
    include_package_data=True,
    zip_safe=False,
    keywords=KEYWORDS
)

