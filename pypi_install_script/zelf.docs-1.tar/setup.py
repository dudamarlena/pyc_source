#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" setup.py """

from setuptools import find_packages, setup

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name='zelf.docs',
    version='1',
    url='https://bitbucket.org/bthate/zelf.docs',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description="framework to program bots.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='Public Domain',
    zip_safe=False,
    install_requires=["zelf"],
    scripts=["bin/zelf-docs", "bin/zelf-rtfd"],
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: Public Domain',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Utilities'
                ]
)
