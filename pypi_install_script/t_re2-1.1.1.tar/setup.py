#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from codecs import open
import os
base_dir = os.path.abspath(os.path.dirname(__file__))


with open(os.path.join(base_dir, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='t_re2',
    version='1.1.1',
    description='faster rules in python',
    long_description=long_description,
    packages=find_packages(),
    include_package_data=True
)
