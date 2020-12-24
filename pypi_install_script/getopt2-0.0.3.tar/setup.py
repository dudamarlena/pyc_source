#!/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 Aleksandar Buza <aleksandar.buza@consulteer.com>
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

from os import path
from setuptools import setup


here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='getopt2',
    version='0.0.3',
    packages=['getopt2'],
    python_requires='>=3.6',
    url='https://github.com/alekbuza/getopt-ng',
    license='License :: OSI Approved :: ISC License (ISCL)',
    author='Aleksandar Buza',
    author_email='aleksandar.buza@consulteer.com',
    classifiers=[
        'License :: OSI Approved :: ISC License (ISCL)',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Operating System :: POSIX :: BSD',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],
    description='Pythonic Unix C-style parser for command line options in few LOC',
    long_description=long_description,
    long_description_content_type="text/markdown"
)
