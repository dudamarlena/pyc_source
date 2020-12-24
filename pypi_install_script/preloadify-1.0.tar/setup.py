#!/usr/bin/env python

import sys, os, shutil
from distutils.core import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='preloadify',
      version='1.0',
      description='Create fat binaries with ease.',
      long_description=long_description,
      author='Tobias Glaesser',
      author_email="tobimensch@gmail.com",
      url='https://github.com/tobimensch/preloadify/',
      scripts=['preloadify'],
      install_requires=['docopt'],
      license='MIT'
     )
