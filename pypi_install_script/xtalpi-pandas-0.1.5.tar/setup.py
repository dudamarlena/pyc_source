#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages

setup(
    name='xtalpi-pandas',
    version='0.1.5',
    author='Wenzhi Ma',
    author_email='wenzhi.ma@xtalpi.com',
    description=u'XtalPi Pandas CMD',
    packages=find_packages(),
    install_requires=['click', 'pandas'],
    entry_points={
        'console_scripts': ['xpandas=xpandas:run']
    }
)
