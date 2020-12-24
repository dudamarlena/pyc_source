#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

long_description = ""
with open('README.rst') as f:
    long_description += f.read()

with open('HISTORY.rst') as f:
    long_description += '\n\n'
    long_description += f.read() .replace('.. :changelog:', '')

setup(
    name='tidalapi4mopidy',
    version='0.1.3',
    description='Unofficial API for TIDAL music streaming service.',
    long_description=long_description,
    author='Thomas Amland, Simone Fantini',
    author_email='thomas.amland@googlemail.com, mones88@gmail.com',
    url='https://github.com/mones88/python-tidal',
    license='LGPL',
    packages=['tidalapi4mopidy'],
    install_requires=['requests', 'pytest'],
    keywords='',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
)
