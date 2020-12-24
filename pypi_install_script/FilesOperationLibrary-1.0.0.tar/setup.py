# -*- coding: utf-8 -*-
"""this package is used to file operation

:copyright: 
:author: leo
:contact: 
"""
import re
import sys
from os.path import abspath, dirname, join
from setuptools import setup

CURDIR = dirname(abspath(__file__))
REQUIREMENTS = ['robotframework >= 2.0']
with open(join(CURDIR, 'README.rst')) as f:
    DESCRIPTION = f.read()
CLASSIFIERS = '''
Development Status :: 5 - Production/Stable
License :: OSI Approved :: Apache Software License
Operating System :: OS Independent
Programming Language :: Python
Programming Language :: Python :: 2.7
Topic :: Software Development :: Testing
Framework :: Robot Framework
Framework :: Robot Framework :: Library
'''.strip().splitlines()

setup(
    name='FilesOperationLibrary',
    version='1.0.0',
    description='Robot Framework test library Files Operation',
    long_description=DESCRIPTION,
    author='leo',
    author_email='liyaowang518@gmail.com',
    url='https://github.com',
    license='Apache License 2.0',
    keywords='robotframework testing testautomation Files Operation',
    platforms='any',
    classifiers=CLASSIFIERS,
    install_requires = REQUIREMENTS,
    package_dir={'':'src'},
    packages=['FilesOperationLibrary']
)