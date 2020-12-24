#!/usr/bin/env python3
"""Setuptools-based setup.py."""

import pathlib
import re
import subprocess

from codecs import open
from setuptools import setup, find_packages

# Check if Java is installed and is the correct version
process = subprocess.run(['java', '-version'], stderr=subprocess.PIPE)
try:
    assert re.match(b'java version "9\..+', process.stderr.splitlines()[0])
except AssertionError:
    print('Please install Java version 9')

# Get the long description from the README file
here = pathlib.Path(__file__).parent
with open(here.joinpath('README.rst'), encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='jreg',
    version='1.0.0',

    description='Python package for using Java regular expressions',
    long_description=long_description,

    url='https://github.com/utkonos/jreg',
    download_url='https://github.com/utkonos/jreg/tarball/1.0.0',

    author='Malware Utkonos',
    author_email='utkonos@malwarolo.gy',
    license='BSD',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],

    keywords='python regex java',

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
)
