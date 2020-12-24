#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" setup.py """

from setuptools import setup

def readme():
    return open("README").read()

setup(
    name='botz.cli',
    version='1',
    url='https://bitbucket.org/bthate/botz.cli',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description="Framework to program bots",
    long_description=readme(),
    license='Public Domain',
    install_depends=["botz"],
    scripts=["bin/botz", "bin/botz-irc", "bin/botz-ps", "bin/botz-stop"],
    classifiers=['Development Status :: 3 - Alpha',
                 'Environment :: Console',
                 'Intended Audience :: Developers',
                 'License :: Public Domain',
                 'Operating System :: Unix',
                 'Programming Language :: Python'
                ]
)
