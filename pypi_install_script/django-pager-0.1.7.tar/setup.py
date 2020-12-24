#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Copyright (c) 2012 Ilya Shalyapin
#
#  django-pager is free software under terms of the MIT License.
#

import os
from setuptools import setup, find_packages


setup(
    name     = 'django-pager',
    version  = '0.1.7',
    packages = find_packages(),
    include_package_data = True,
    requires = ['python (>= 2.5)', 'django (>= 1.0)'],
    description  = 'Pagination.',
    long_description = open('README.markdown').read(),
    author       = 'Ilya Shalyapin',
    author_email = 'ishalyapin@gmail.com',
    url          = 'https://github.com/un1t/django-pager',
    download_url = 'https://github.com/un1t/django-pager/tarball/master',
    license      = 'MIT License',
    keywords     = 'django',
    classifiers  = [
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
    ],
)
