#!/usr/bin/env python                                                            
# encoding: UTF-8

from distutils.core import setup

setup(
    name = 'continuum',
    version = '0.1.2',
    author = 'Michel Casabianca',
    author_email = 'casa@sweetohm.net',
    packages = ['continuum'],
    url = 'http://pypi.python.org/pypi/continuum/',
    license = 'Apache Software License',
    description = 'continuum is a minimalist continuous integration tool',
    long_description=open('README.rst').read(),
    entry_points = {
        'console_scripts': [
            'continuum = continuum:run',
        ],
    },
)

