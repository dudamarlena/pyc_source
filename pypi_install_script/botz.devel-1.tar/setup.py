#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" setup.py """

from setuptools import setup

def readme():
    return open("README").read()

setup(
    name='botz.devel',
    version='1',
    url='https://bitbucket.org/bthate/botz.devel',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description="Framework to program bots",
    long_description=readme(),
    license='Public Domain',
    install_depends=["botz"],
    scripts=["bin/botz-do",
             "bin/botz-doctests",
             "bin/botz-lint",
             "bin/botz-rtfd",
             "bin/botz-sed",
             "bin/botz-test"],
    classifiers=['Development Status :: 3 - Alpha',
                 'Environment :: Console',
                 'Intended Audience :: Developers',
                 'License :: Public Domain',
                 'Operating System :: Unix',
                 'Programming Language :: Python'
                ]
)
