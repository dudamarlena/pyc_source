#!/usr/bin/env python

import glob
from setuptools import setup, find_packages


setup(
    name='dorothy',
    description='Boilerplate code for a web and/or API application written using Tornado.',
    packages=[
        'dorothy',
        'dorothy.lib'
    ],
    version='0.1.10',
    author='Travis Beauvais',
    author_email='tbeauvais@gmail.com',
    url='https://github.com/MrTravisB/dorothy',
    keywords='tornado boilerplate api web',
    install_requires=[
        'tornado>=3.1',
        'pyyaml>=3.10',
    ]
)
