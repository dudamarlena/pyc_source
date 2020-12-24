#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from distutils.core import setup


setup(
    name = 'dongu',
    version = '1.0.0',
    keywords = 'pipeline',
    description = 'Simple Python pipelines.',
    license = 'MIT',
    author = 'Ertugrul Keremoglu',
    author_email = 'ertugkeremoglu@gmail.com',
    url = 'https://github.com/ertgl/dongu/',
    classifiers = [
        'Topic :: Utilities',
        'Intended Audience :: Developers',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
    ],
    packages = [
        'dongu',
        'dongu.abstract',
    ],
)
