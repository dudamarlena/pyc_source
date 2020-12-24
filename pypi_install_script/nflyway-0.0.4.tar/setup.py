#! /usr/bin/env python
# -*- coding: utf-8 -*_
# Author: nie<bellondragon@gmail.com>
from distutils.core import setup
import setuptools

setup(
    name='nflyway',
    version='0.0.4',
    description='this package is used to migrate db in project',
    author='nie',
    author_email='bellondragon@gmail.com',
    url='',
    packages=setuptools.find_packages(exclude=['test', 'examples', 'script', 'tutorials']),

    install_requires=[
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],
    zip_safe=True,
)
