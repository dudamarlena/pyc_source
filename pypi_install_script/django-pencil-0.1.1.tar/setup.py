#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Copyright (c) 2012 Ilya Shalyapin
#
#  django-pencil is free software under terms of the MIT License.
#

import os
from setuptools import setup


setup(
    name     = 'django-pencil',
    version  = '0.1.1',
    packages = ['django_pencil'],

    requires = ['python (>= 2.5)', 'django (>= 1.3)'],

    description  = 'Intergetion Pencil WYSIWYG into Django.',
    long_description = open('README.markdown').read(),
    author       = 'Ilya Shalyapin',
    author_email = 'ishalyapin@gmail.com',
    url          = 'https://github.com/un1t/django-pencil',
    download_url = 'https://github.com/un1t/django-pencil/tarball/master',
    license      = 'MIT License',
    keywords     = 'django pencil wysiwyg',
    classifiers  = [
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
    ],
)
