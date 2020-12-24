#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" setup.py """

import os
import sys

if sys.version_info.major < 3:
    print("you need to run BOHT with python3")
    os._exit(1)

try:
    use_setuptools()
except:
    pass

try:
    from setuptools import setup
except Exception as ex:
    print(str(ex))
    os._exit(1)

setup(
    name='boht',
    version='2',
    url='https://bitbucket.org/bthate/boht',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description="boht is an irc bot.",
    long_description="""
BOHT is a pure python3 framework to program bots (a botlib), provides an IRC bot to use and is extendible by programming your own commands.
BOHT uses a timestamped, type in filename, JSON stringified, files on filesystem backend and has timed based logging capabilities.
BOHT has been placed in the Public Domain and contains no copyright or LICENSE.
    """,
    license='Public Domain',
    zip_safe=True,
    install_requires=[""],
    scripts=["bin/boht"],
    packages=['boht'],
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: Public Domain',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Utilities'
                ]
)
