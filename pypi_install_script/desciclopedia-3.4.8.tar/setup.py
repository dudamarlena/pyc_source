# -*- coding: utf-8 -*-
import codecs
import os
import re
import setuptools


def local_file(file):
  return codecs.open(
    os.path.join(os.path.dirname(__file__), file), 'r', 'utf-8'
  )

setuptools.setup(
  name = "desciclopedia",
  version = '3.4.8',
  author = "Jonathan Goldsmith",
  author_email = "jhghank@gmail.com",
  description = "desciclopedia API for Python",
  license = "MIT",
  keywords = "python wikipedia API",
  url = "https://github.com/goldsmith/Wikipedia",
  install_requires = ['beautifulsoup4','requests>=2.0.0,<3.0.0'],
  packages = ['desciclopedia'],
  long_description = local_file('README.rst').read(),
  classifiers = [
    'Development Status :: 4 - Beta',
    'Topic :: Software Development :: Libraries',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3'
  ]
)
