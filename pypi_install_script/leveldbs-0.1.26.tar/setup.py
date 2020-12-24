#!/usr/bin/env python3
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: InfinityFuture
# Mail: infinityfuture@foxmail.com
# Created Time: 2018-08-09 02:00:00
#############################################

import os
from setuptools import setup, find_packages

version = os.path.join(
    os.path.realpath(os.path.dirname(__file__)),
    'version.txt'
)

setup(
    name = 'leveldbs',
    version = open(version, 'r').read().strip(),
    keywords = ('pip', 'leveldb'),
    description = 'time and path tool',
    long_description = 'time and path tool',
    license = 'MIT Licence',

    url = 'https://github.com/infinityfuture/leveldb-server',
    author = 'infinityfuture',
    author_email = 'infinityfuture@foxmail.com',

    packages = find_packages(),
    include_package_data = True,
    platforms = 'any',
    install_requires = ['pyzmq']
)