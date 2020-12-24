#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" setup.py """

from setuptools import setup

def readme():
    return open("README").read()

setup(
    name='botz',
    version='15',
    url='https://bitbucket.org/bthate/botz',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description="Framework to program bots",
    long_description=readme(),
    license='Public Domain',
    packages=["botz"],
    zip_safe=False,
    classifiers=['Development Status :: 3 - Alpha',
                 'Environment :: Console',
                 'Intended Audience :: Developers',
                 'License :: Public Domain',
                 'Operating System :: Unix',
                 'Programming Language :: Python'
                ]
)
