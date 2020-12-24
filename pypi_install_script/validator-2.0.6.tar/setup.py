#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

__major__   = 2
__minor__   = 0
__patch__   = 6
__version__ = '.'.join([str(__major__), str(__minor__), str(__patch__)])

setup(
    name='validator',
    version=__version__,
    description='A plain-as-vanilla validating package written for Python.',
    author='Wilhelm Murdoch',
    author_email='wilhelm.murdoch@gmail.com',
    url='https://github.com/wilhelm-murdoch/validator',
    packages=find_packages(exclude=['tests', 'tests.*']),
    setup_requires=[
          'nose==1.3.1'
        , 'yanc==0.2.4'
    ]
)
