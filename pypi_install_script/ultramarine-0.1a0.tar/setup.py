#!/usr/bin/env python
# encoding: utf-8
from __future__ import absolute_import, print_function
import os
from setuptools import setup, find_packages
from ultramarine.version import __version__


__author__ = 'Dmitry Orlov <me@mosquito.su>'


setup(
    name='ultramarine',
    version=__version__,
    author=__author__,
    author_email='me@mosquito.su',
    license="LGPLv3",
    description="PyUV-based asynchronous library",
    platforms="all",
    classifiers=[
        'Environment :: Console',
        'Programming Language :: Python',
    ],
    long_description=open('README.rst').read(),
    packages=find_packages(),
    install_requires=[r.strip(' ') for r in open('requirements.txt').read().split('\n')],
)
