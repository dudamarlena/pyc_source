#!/usr/bin/env python

# Copyright 2009 Canonical Ltd.  All rights reserved.
#
# This file is part of lazr.batchnavigator
#
# lazr.batchnavigator is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# lazr.batchnavigator is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public
# License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with lazr.batchnavigator. If not, see <http://www.gnu.org/licenses/>.

import re

from setuptools import setup, find_packages

# generic helpers primarily for the long_description
def generate(*docname_or_string):
    res = []
    for value in docname_or_string:
        if value.endswith('.rst'):
            with open(value) as f:
                value = f.read()
                # toctree is a Sphinx extension.
                value = re.sub(
                    r'^\.\. toctree::\n.*?(?=^\S|\Z)', '', value,
                    flags=re.M | re.S)
        res.append(value)
        if not value.endswith('\n'):
            res.append('')
    return '\n'.join(res)
# end generic helpers

__version__ = open("src/lazr/batchnavigator/version.txt").read().strip()

tests_require = [
    'testtools',
    'zope.publisher',
    'zope.testrunner',
    ]

setup(
    name='lazr.batchnavigator',
    version=__version__,
    namespace_packages=['lazr'],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    maintainer='LAZR Developers',
    maintainer_email='lazr-users@lists.launchpad.net',
    description=open('README.rst').readline().strip(),
    long_description=generate(
        'src/lazr/batchnavigator/docs/index.rst',
        'NEWS.rst'),
    license='LGPL v3',
    install_requires=[
        'setuptools',
        'six',
        'zope.cachedescriptors',
        'zope.interface>=3.6.0',
        ],
    url='https://launchpad.net/lazr.batchnavigator',
    download_url='https://launchpad.net/lazr.batchnavigator/+download',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        ],
    tests_require=tests_require,
    extras_require=dict(
        docs=['Sphinx'],
        test=tests_require,
    ),
    test_suite='lazr.batchnavigator.tests',
    )
