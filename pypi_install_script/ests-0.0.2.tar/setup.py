#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from setuptools import find_packages, setup

readme = open('README.md').read()

install_requires = [
    'pandas',
    'numpy',
    'colorednoise',
    'rpy2',
    'scikit-learn',
    'fitter'
]

packages = find_packages()

g = {}
with open(os.path.join('ets', 'version.py'), 'rt') as fp:
    exec(fp.read(), g)
    version = g['__version__']

setup(
    name='ests',
    version=version,
    packages=packages,
    author="Felipe Carlos",
    author_email="felipe.carlos@inpe.br",
    include_package_data=True,
    description="Tool to facilitate the realization of educational activities of statistical and spectral analysis of stochastic processes",
    long_description=readme,
    long_description_content_type='text/markdown',
    install_requires=install_requires,
)
