#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -*- mode: python -*-
import os
import sys

from setuptools import setup, find_packages


'''

VERSION  HISTORY

0.0.1 - Primeira instalação
0.0.2 - Registrando cobrança

'''

__version__ = '0.0.2'


here =os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file
with open(os.path.join(here, 'README.rst')) as f:
    long_description = f.read()

setup(
    name = 'pyf2b',
    version = __version__,
    packages = find_packages(),
    script_name = 'setup.py',
    scripts = [],

    package_data = {
        "base": ["VERSION"],
    },
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3', 
    ],
    # metadata for upload to PyPI
    author = 'William Marquardt',
    author_email = 'williammqt@gmail.com',
    description = 'Python lib that consume F2b API.',
    long_description = long_description,
    license = 'MIT',
    keywords = 'python f2b cobranca',
    url = 'https://github.com/wmarquardt/pyf2b',
    install_requires=[
        'requests',
    ],
)
