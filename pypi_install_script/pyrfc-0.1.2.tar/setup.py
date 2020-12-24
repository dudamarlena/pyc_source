#! /usr/bin/env python
# coding: utf-8

#  __author__ = 'meisanggou'

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import sys

if sys.version_info <= (2, 7):
    sys.stderr.write("ERROR: jingyun tools requires Python Version 2.7 or above.\n")
    sys.stderr.write("Your Python Version is %s.%s.%s.\n" % sys.version_info[:3])
    sys.exit(1)

name = "pyrfc"
version = "0.1.2"
url = "https://github.com/meisanggou/rfc"
license = "MIT"
author = "meisanggou"
short_description = "Implementation of some RFC standard algorithms"
long_description = """
Implementation of some RFC standard algorithms. Now Include RFC2548 RFC2759 RFC3078 RFC3079
"""
keywords = "rfc2"
install_requires = []

setup(name=name,
      version=version,
      author=author,
      author_email="zhou5315938@163.com",
      url=url,
      packages=["pyrfc"],
      license=license,
      description=short_description,
      long_description=long_description,
      keywords=keywords,
      install_requires=install_requires
      )
