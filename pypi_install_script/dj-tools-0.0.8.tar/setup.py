#!/usr/bin/env python

import os
from setuptools import setup, find_packages

import dj_tools


PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

desc = open(os.path.join(PROJECT_ROOT, 'README.md')).read()
lic = open(os.path.join(PROJECT_ROOT, 'LICENSE')).read()

requires = [
    'Django >= 1.5.1',
]

setup(
    name='dj-tools',
    version=dj_tools.__version__,
    description='Django reusable tools',
    long_description=desc,
    author='Andrei Petre',
    author_email='me@andreipetre.com',
    url='https://github.com/andreipetre/dj-tools',
    install_requires=requires,
    packages=find_packages(),
    license=lic,
    zip_safe=False,
)
