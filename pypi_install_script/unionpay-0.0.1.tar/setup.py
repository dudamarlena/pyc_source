#! /usr/bin/env python
# encoding: utf-8

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
# To use a consistent encoding
from codecs import open
from os import path
import sys

here = path.abspath(path.dirname(__file__))


setup(
    name='unionpay',
    version='0.0.1',
    keywords='unionpay',
    description='unionpay',
    long_description='unionpay',
    url='https://github.com/007gzs/unionpay',
    author='007gzs',
    author_email='007gzs@sina.com',
    license='LGPL v3',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: '
        'GNU Lesser General Public License v3 (LGPLv3)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    packages=find_packages(exclude=('tests', 'tests.*')),
    install_requires=[],
    zip_safe=False,
    include_package_data=True
)
