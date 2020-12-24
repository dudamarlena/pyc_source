#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages

setup(
    name='posit',
    version='0.1.2',
    author='Wenzhi Ma',
    author_email='wenzhi.ma@xtalpi.com',
    description=u'Pick a pose',
    packages=find_packages(),
    install_requires=['click'],
    entry_points={
        'console_scripts': ['posit=Posit:run']
    }
)
