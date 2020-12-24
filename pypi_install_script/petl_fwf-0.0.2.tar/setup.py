#!/usr/bin/env python
# -*- coding: utf-8 -*-
# MIT copyright
from __future__ import (print_function, unicode_literals)
from builtins import str

from ast import literal_eval
from setuptools import setup

def get_version(source='petl_fwf/__pkginfo__.py'):
    with open(source) as f:
        for line in f:
            if line.startswith('__version__'):
                return literal_eval(line.split('=')[-1].lstrip())
    raise ValueError("__version__ not found")

setup(
    name='petl_fwf',
    version=get_version(),
    author='JoBrad',
    author_email='jtbradley+petlfwf@gmail.com',
    package_dir={'': '.'},
    packages=['petl_fwf', 'petl_fwf.test'],
    install_requires=['petl'],
    tests_require=['nose'],
    url='https://github.com/JoBrad/petl_fwf',
    license='MIT License',
    description='Additional methods for the petl library that enable reading fixed-width files',
    long_description=open('README.md').read(),
    python_requires='>=2.7',
    keywords='petl fixed-width text',
    classifiers=['Intended Audience :: Developers',
                 'License :: OSI Approved :: MIT License',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.4',
                 'Programming Language :: Python :: 3.5',
                 'Programming Language :: Python :: 3.6',
                 'Topic :: Software Development :: Libraries :: Python Modules'
                 ]
)