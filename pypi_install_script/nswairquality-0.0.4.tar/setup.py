#!/usr/bin/env python
from distutils.core import setup
import sys

for cmd in ('egg_info', 'develop'):
    if cmd in sys.argv:
        from setuptools import setup

setup_args = dict(
    name = 'nswairquality',
    version = '0.0.4',
    author = 'Troy Kelly',
    author_email = 'troy@troykelly.com',
    url = 'https://github.com/troykelly/python-nswairquality',

    description = 'NSW Air Quality Scraper',
    long_description = open('README.rst').read(),
    license = 'Creative Commons Attribution-Noncommercial-Share Alike license',

    package_dir = {'': 'src'},
    py_modules = ['nswairquality'],
    install_requires=['requests','BeautifulSoup',],

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)

setup(**setup_args)
