#!/usr/bin/env python
#
# The MIT License (MIT)
#
# Copyright (c) 2020 Philippe Proulx <eepp.ca>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


import sys
from setuptools import setup


# make sure we run Python 3+ here
v = sys.version_info

if v.major < 3:
    sys.stderr.write('Sorry, qngng needs Python 3\n')
    sys.exit(1)


import qngng


setup(name='qngng',
      version=qngng.__version__,
      description=qngng.__description__,
      author='Philippe Proulx',
      author_email='eeppeliteloop@gmail.com',
      url='https://github.com/eepp/qngng',
      packages=['qngng'],
      package_data={
          'qngng': ['cats/*.json'],
      },
      install_requires=['setuptools'],
      entry_points={
          'console_scripts': [
              'qngng = qngng.qngng:_main',
          ]
      },
      classifiers=[
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Environment :: Console',
          'Intended Audience :: System Administrators',
          'Natural Language :: English',
          'Programming Language :: Python :: 3 :: Only',
      ])
