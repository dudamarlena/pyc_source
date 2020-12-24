#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" setup.py """

from setuptools import find_packages, setup

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name='zelf',
    version='10',
    url='https://bitbucket.org/bthate/zelf',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description="framework to program bots.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='Public Domain',
    zip_safe=False,
    scripts=["bin/zelf"],
    packages=["zelf"],
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: Public Domain',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Utilities'
                ]
)
