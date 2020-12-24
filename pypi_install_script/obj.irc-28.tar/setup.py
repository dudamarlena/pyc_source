#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# OBJ.IRC - OBJ package you can use to program IRC bots.
#
# setup.py

""" setup.py """

import os
import sys

if sys.version_info.major < 3:
    print("you need to run OBJ.IRC with python3")
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

def readme():
    return open("README").read()

setup(
    name='obj.irc',
    version='28',
    url='https://bitbucket.org/bthate/obj.irc',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description="OBJ package you can use to program IRC bots",
    long_description=readme(),
    license='Public Domain',
    include_package_data=True,
    zip_safe=False,
    install_requires=["obj"],
    packages=["obj.irc"],
    scripts=["bin/obj-irc"],
    data_files=[("", ("README",))],
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: Public Domain',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Utilities'
                ]
)
