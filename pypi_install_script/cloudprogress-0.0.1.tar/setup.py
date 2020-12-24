#!/usr/bin/env python3

import os
from distutils.core import setup
from setuptools import find_packages

setup(
  name='cloudprogress',
  version=open(os.path.join(os.path.dirname(__file__), 'cloudprogress', 'VERSION')).read().strip(),
  description="Python rest client for Cloud Progress https://cloudprogress.io, ",
  author="Abe Winter",
  author_email="awinter.public+cprpy@gmail.com",
  url="https://github.com/cloudprogress/cpr-py",
  packages=find_packages(include=['cloudprogress', 'cloudprogress.*']),
  keywords=['cloudprogress', 'progress bar', 'progress', 'loading bar', 'eta'],
  install_requires=[
    'requests==2.22.0',
  ],
  python_requires='>=3.7', # 3.6 for format strings, 3.7 for dataclasses
  long_description=open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
  long_description_content_type='text/markdown',
)
