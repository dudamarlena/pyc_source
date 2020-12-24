#!/usr/bin/env python
# encoding=utf-8

import os
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

BASE_DIR = os.path.dirname(__file__)

about = {}
with open(os.path.join(BASE_DIR, 'xtls', '__about__.py')) as f:
    exec(f.read(), about)

with open(os.path.join(BASE_DIR, 'README.rst'), 'rb') as f_readme:
    README = f_readme.read()

PACKAGES = ['xtls']

setup(
    name=about['__name__'],
    version=about['__version__'],
    keywords=['xlzd', 'python', 'python tools'],
    description=about['__summary__'],
    long_description=README,
    author=about['__author__'],
    author_email=about['__email__'],
    license=about['__license__'],
    url=about['__url__'],
    download_url=about['__download_url__'],
    install_requires=about['__requires__'],
    extras_require={},
    packages=PACKAGES,
    classifiers=[]
)
