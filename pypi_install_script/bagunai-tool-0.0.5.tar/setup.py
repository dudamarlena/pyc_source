#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name = 'bagunai-tool',
    version = '0.0.5',
    keywords = ['pip', 'tool', 'bagunai'],
    description = 'Tool package',
    license = 'MIT Licence',

    url = 'https://github.com/viger1228',
    author = 'walker',
    author_email = 'walkerIVI@gmail.com',

    packages = find_packages(),
    include_package_data = True,
    platforms = 'any',
    install_requires = ['requests']
)
