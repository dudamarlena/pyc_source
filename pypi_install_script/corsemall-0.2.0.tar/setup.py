#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

requisites = ['flask>=1.0.0']

setup(
    name='corsemall',
    version='0.2.0',
    description='Serves JSON data with CORS allowed from *.json files at given path.',
    long_description=open('README.rst').read(),
    author='Viet Hung Nguyen',
    author_email='hvn@familug.org',
    url='https://github.com/hvnsweeting/corsemall',
    py_modules=['corsemall'],
    license='MIT',
    install_requires=requisites,
    entry_points={'console_scripts': ['corsemall=corsemall:cli']},
    classifiers=[
        'Environment :: Console',
        'Topic :: Terminals :: Terminal Emulators/X Terminals',
    ],
)
