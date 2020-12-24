# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from setuptools import setup, find_packages

with open('README.rst') as f:
    README = f.read()

setup(
    name='mozautomation',
    version='0.1',
    packages=find_packages(),
    description=('Provides client libraries and other functionality used '
        'by numerous Mozilla projects.'),
    long_description=README,
    author='Gregory Szorc',
    author_email='gps@mozilla.com',
)
