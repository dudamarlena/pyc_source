#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from codecs import open
import os
import shutil
base_dir = os.path.abspath(os.path.dirname(__file__))

# copy so file to /usr/local/lib
dependent_files = '/usr/local/lib/libre2.so.7'
if not os.path.isfile(dependent_files):
    if os.path.exists(os.path.dirname(dependent_files)):
        os.makedirs(os.path.dirname(dependent_files))
    shutil.copy2('./libre2.so.7', dependent_files)


with open(os.path.join(base_dir, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='py-re2',
    version='1.0.0',
    description='faster rules in python',
    long_description=long_description,
    packages=find_packages(exclude=[]),
    include_package_data=True,
)