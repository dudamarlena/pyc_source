#!/usr/bin/env python
# -*- coding: utf-8 -*-
##############################################################################
# The MIT License (MIT)

# Copyright (c) 2015 Augustin Cisterne-Kaas

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
##############################################################################
from setuptools import setup


with open('README.rst') as f:
    readme = f.read()

tests_require = ['mock', 'unittest2', 'argparse'],
test_suite = 'unittest2.collector'

setup(
    name="docker-postgres-client",
    version="0.0.2",
    author="Augustin Cisterne-Kaas",
    author_email="ajitekun@gmail.com",
    description=(
        'Client that uses the PostgreSQL client inside a Docker container.'),
    platforms='any',
    license='MIT',
    py_modules=['docker_postgres_client', 'dpsql', 'dpg_dump', 'dcreatedb',
                'ddropdb'],
    entry_points={
        'console_scripts': [
            'dpsql = dpsql:main',
            'dpg_dump = dpg_dump:main',
            'dcreatedb = dcreatedb:main',
            'ddropdb = ddropdb:main',
        ]
    },
    keywords="docker postgres",
    url='http://packages.python.org/docker-postgres-client',
    long_description=readme,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    tests_require=tests_require,
    test_suite=test_suite
)
