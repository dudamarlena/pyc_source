#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Copyright (c) 2012 Ilya Shalyapin
#
#  python-debug is free software under terms of the MIT License.
#

import os
from setuptools import setup, find_packages


setup(
    name     = 'python-debug',
    version  = '0.1.3',
    packages = find_packages(),
    requires = ['python (>= 2.5)'],
    description  = 'Useful debugging tools.',
    long_description = open('README.markdown').read(),
    author       = 'Ilya Shalyapin',
    author_email = 'ishalyapin@gmail.com',
    url          = 'https://github.com/un1t/python-debug',
    download_url = 'https://github.com/un1t/python-debug/tarball/master',
    license      = 'MIT License',
    keywords     = 'django',
    classifiers  = [
        'Intended Audience :: Developers',
        'Programming Language :: Python',
    ],
)
