#!/usr/bin/env python
# -*- coding: utf-8 -*-
import io
import re
from setuptools import setup, find_packages

kwargs = {}

with io.open('README.rst', 'rt', encoding='utf8') as f:
    readme = f.read()

with io.open('pylib/__init__.py', 'rt', encoding='utf8') as f:
    version = re.search(r"__version__ = \'(.*?)\'", f.read()).group(1)

setup(
    name='lx-pylib',
    version=version,
    description='Some useful python utils',
    long_description=readme,
    author='Larry Xu',
    author_email='hilarryxu@gmail.com',
    url='https://github.com/hilarryxu/lx-pylib',
    license='BSD',
    packages=find_packages(exclude=['test*', 'docs', 'examples']),
    include_package_data=True,
    **kwargs
)
