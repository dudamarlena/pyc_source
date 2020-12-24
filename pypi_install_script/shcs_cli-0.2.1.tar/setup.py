#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Setup for shcs_cli
"""

import os
from setuptools import setup, find_packages

import shcs_cli

NAME = "shcs_cli"
VERSION = shcs_cli.__version__
DESC = "shcs_cli client for shcs server"
URLPKG = "https://github.com/fraoustin/shcs_cli.git"

HERE = os.path.abspath(os.path.dirname(__file__))

# README AND CHANGES
with open(os.path.join(HERE, 'README.rst')) as readme:
    with open(os.path.join(HERE, 'CHANGES.rst')) as changelog:
        LONG_DESC = readme.read() + '\n\n' + changelog.read()
# REQUIREMENTS
with open('REQUIREMENTS.txt') as f:
    REQUIRED = f.read().splitlines()
# CLASSIFIERS
with open('CLASSIFIERS.txt') as f:
    CLASSIFIED = f.read().splitlines()
# AUTHORS
with open('AUTHORS.txt') as f:
    DATA = f.read().splitlines()
    AUTHORS = ','.join([i.split('::')[0] for i in DATA])
    AUTHORS_EMAIL = ','.join([i.split('::')[1] for i in DATA])

setup(
    name=NAME,
    version=VERSION,
    packages=find_packages(),
    author=AUTHORS,
    author_email=AUTHORS_EMAIL,
    description=DESC,
    long_description=LONG_DESC,
    include_package_data=True,
    install_requires=REQUIRED,
    url=URLPKG,
    classifiers=CLASSIFIED,
    entry_points = {
        'console_scripts': [
            'shcs-cli = shcs_cli.main:main',
        ],
    },
)
