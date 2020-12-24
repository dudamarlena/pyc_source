# -*- coding: utf-8 -*-
# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# io.open is needed for projects that support Python 2.7
# It ensures open() defaults to text mode with universal newlines,
# and accepts an argument to specify the text encoding
# Python 3 only projects can skip this import
from io import open



with open("README.md",'r', encoding='UTF-8') as fh:
    long_description = fh.read()
    
# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.
setup(
    name = 'trafficconflict',
    version = '0.3.6',
    description = 'a library for traffic conflict detection and analysis from swjtu_102',
    license = 'MIT License',
    url = '',
    author = 'swjtu_102',
    author_email = '',
    packages = find_packages(),
    include_package_data = True,
    platforms = 'any',
    install_requires = [],
    )