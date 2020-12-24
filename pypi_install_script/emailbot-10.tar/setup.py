#!/usr/bin/env python3
""" EMAILBOT - email correspondence analysis. """

import os
import sys

if sys.version_info.major < 3:
    print("you need to run EMAILBOT with python3")
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
    name='emailbot',
    version='10',
    url='https://bitbucket.org/botd/emailbot',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description="email correspondence analysis.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    license='Public Domain',
    install_requires=["libobj"],
    scripts=["bin/emailbot"],
    packages=["emailbot"],
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: Public Domain',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Utilities'
                ]
)
