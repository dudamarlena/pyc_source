#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('requirements.txt') as f:
    requires = f.readlines()

setup(
    name='tds-python-redis-rate-limit',
    version='0.0.6',
    description=u'Python Rate Limiter based on Redis.',
    long_description=readme,
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=requires
)
