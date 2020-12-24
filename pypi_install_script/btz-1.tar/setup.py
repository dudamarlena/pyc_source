#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" setup.py """

from setuptools import setup

def readme():
    return open("README").read()

setup(
    name='btz',
    version=1,
    url='https://bitbucket.org/bthate/btz',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description="Framework to program bots",
    long_description=readme(),
    zip_safe=False,
    license='Public Domain',
    packages=["btz"],
    scripts=["bin/btz"],
    classifiers=['Development Status :: 3 - Alpha',
                 'Environment :: Console',
                 'Intended Audience :: Developers',
                 'License :: Public Domain',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Software Development :: Libraries :: Application Frameworks'
                ]
)
