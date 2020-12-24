#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name = 'django-translatable',
    packages = ['translatable',],
    version = '0.1.1',
    description = "Django app providing simple translatable models system",
    author = "Mikołaj Siedlarek",
    author_email = 'mikolaj.siedlarek@gmail.com',
    url = 'https://github.com/mikoskay/django-translatable',
    install_requires=[
        'Django>=1.2',
    ],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Internationalization',
    ]
)
        

