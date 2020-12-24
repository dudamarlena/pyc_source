#!/usr/bin/env python

from setuptools import setup, find_packages
setup(name='Data_validation_v1',
version='1.4',
description='Data Validation package',
author='Afiz Oyerinde',
author_email='ayodejioyerinde93@gmail.com',
license='Free',
packages=['data_validation',],
scripts=['data_validation/data_validation.py'],
classifiers = ['Programming Language :: Python :: 3'],
install_requires = ['pandas', 'numpy'],
zip_safe=False)
