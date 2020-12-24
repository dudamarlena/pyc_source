#!/usr/bin/env python3
""" UDPBOT - udp to IRC channel relay. """

import os
import sys

if sys.version_info.major < 3:
    print("you need to run UDPBOT with python3")
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

with open('README') as file:
    long_description = file.read()

setup(
    name='udpbot',
    version='2',
    url='https://github.com/bthate/udpbot',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description="udp to IRC channel relay",
    long_description=long_description,
    license='Public Domain',
    install_requires=["obot"],
    scripts=["bin/udpbot"],
    packages=["udpbot"],
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: Public Domain',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Utilities'
                ]
)
