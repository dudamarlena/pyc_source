#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Copyright (c) 2012 Ilya Shalyapin, www.ishalyapin.ru
#
#  dt is free software under terms of the MIT License.
#

import os
from setuptools import setup, find_packages


setup(
    name     = 'dt',
    version  = '0.2',
    packages = find_packages(),
    requires = ['python (>= 2.5)'],
    description  = 'Debug Tools for Python.',
    long_description = open('README.rst').read(),
    author       = 'Ilya Shalyapin',
    author_email = 'ishalyapin@gmail.com',
    url          = 'https://bitbucket.org/ishalyapin/dt',
    license      = 'MIT License',
    classifiers  = [
        'Intended Audience :: Developers',
        'Programming Language :: Python',
    ],
)
