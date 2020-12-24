#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from setuptools import setup

readme = open('README.rst').read()
version = (0, 1, 4)

setup(
    name='abjadtools',
    python_requires=">=3.7",
    version=".".join(map(str, version)),
    description='Utilities to work with abjad and convert to music21',
    long_description=readme,
    author='Eduardo Moguillansky',
    author_email='eduardo.moguillansky@gmail.com',
    url='https://github.com/gesellkammer/emlib',
    packages=[
        'abjadtools',
    ],
    include_package_data=True,
    install_requires=[
        "abjad>=3.1",
        "abjad-ext-nauert @ https://github.com/Abjad/abjad-ext-nauert/tarball/master"
        "abjad-ext-nauert>=3.1"
        "music21",
                
    ],
    license="BSD",
    zip_safe=False,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],
)
