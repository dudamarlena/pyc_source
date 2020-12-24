#!/usr/bin/env python

# Copyright (c) 2015, Mark Fox <markpfox@gmail.com>
# All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish, dis-
# tribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the fol-
# lowing conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABIL-
# ITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
# SHALL THE AUTHOR BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

from __future__ import print_function

dependencies = ['beautifulsoup4',
                'lxml',
                'requests']

try:
    from setuptools import setup
    extra = dict(test_suite="tests.test.suite",
                 include_package_data=True,
                 install_requires=dependencies)
except ImportError:
    from distutils.core import setup
    extra = dict(requires=dependencies)

import sys

from xray import __version__

if sys.version_info <= (2, 6):
    error = "ERROR: x_ray requires Python Version 2.7 or above...exiting."
    print(error, file=sys.stderr)
    sys.exit(1)


def readme():
    with open("README.rst") as f:
        return f.read()

setup(name="x_ray",
      version=__version__,
      description="Chat parser discovering mentions, emoticons, and tags",
      long_description=readme(),
      author="Mark Fox",
      author_email="markpfox@gmail.com",
      scripts=[],
      url="https://github.com/MarkMarine/xray/",
      packages=["xray"],
      package_data={},
      license="MIT",
      platforms="Posix; MacOS X",
      classifiers=["Development Status :: 4 - Beta",
                   "Intended Audience :: Developers",
                   "License :: OSI Approved :: MIT License",
                   "Operating System :: OS Independent",
                   "Topic :: Internet",
                   "Programming Language :: Python :: 2",
                   "Programming Language :: Python :: 2.7"],
      **extra
      )
