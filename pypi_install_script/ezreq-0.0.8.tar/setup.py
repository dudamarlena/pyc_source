#!/usr/bin/env python

# https://github.com/pypa/sampleproject

__name__ = "ezreq"
__author__ = "urain39"
__email__ = "urain39@qq.com"
__version__ = "0.0.8"
__license__ = "MIT"


# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# Description
with open('README') as fp:
    long_description = fp.read()

# Requirements
with  open('requirements.txt') as fp:
    requirements = fp.read().splitlines()

setup(name=__name__,
      version=__version__,
      description='Easy HttpClient Component for Python',
      long_description=long_description,
      author=__author__,
      author_email=__email__,
      license=__license__,
      keywords=['request', 'requests', "http", "httpclient"],
      url='https://github.com/urain39/EzReq',
      packages=find_packages(exclude=['contrib', 'docs', 'tests']),
      install_requires=[requirements],
      platforms='any',
      classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Topic :: Internet"
        ],
     )
