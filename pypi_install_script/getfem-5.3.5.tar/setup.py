#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
import os

from setuptools import setup, find_packages

try:
    with open('README.rst') as f:
        readme = f.read()
except IOError:
    readme = ''

def _requires_from_file(filename):
    return open(filename).read().splitlines()

# version
here = os.path.dirname(os.path.abspath(__file__))
version = next((line.split('=')[1].strip().replace("'", '')
                for line in open(os.path.join(here,
                                              'getfem',
                                              '__init__.py'))
                if line.startswith('__version__ = ')),
               '5.3.5')

setup(
    name="getfem",
    version=version,
    url='http://getfem.org',
    author='Julien Pommier',
    author_email='tkoyama010@gmail.com',
    maintainer='Tetsuo Koyama',
    maintainer_email='tkoyama010@gmail.com',
    description='An open-source finite element library',
    long_description=readme,
    packages=find_packages(),
    install_requires=[
        'scipy'
    ],
    license="LGPLv3",
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    ],
)
