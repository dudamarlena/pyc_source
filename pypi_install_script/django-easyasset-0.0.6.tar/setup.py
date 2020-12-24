#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Copyright (c) 2015 Ilya Shalyapin
#
#  django-easyasset is free software under terms of the MIT License.
#

import os
from setuptools import setup, find_packages


setup(
    name='django-easyasset',
    version='0.0.6',
    packages=['easyasset'],
    install_requires=['csscompressor', 'jsmin', 'six'],
    description='Asset manager.',
    author='Ilya Shalyapin',
    author_email='ishalyapin@gmail.com',
    url='https://github.com/un1t/django-easyasset',
    license='MIT License',
    keywords='django',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
)
