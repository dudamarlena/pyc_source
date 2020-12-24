#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name = 'django-testcoverage',
    packages = ['testcoverage',],
    version = '0.1.3',
    description = "Code coverage reports for Django unit testing framework",
    author = "Mikołaj Siedlarek",
    author_email = 'mikolaj.siedlarek@gmail.com',
    url = 'https://github.com/mikoskay/django-testcoverage',
    install_requires=[
        'Django>=1.2',
        'coverage>=3.4',
    ],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Testing',
    ]
)
        

