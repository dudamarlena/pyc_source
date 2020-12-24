#!/usr/bin/env python

import sys, os, shutil
from distutils.core import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()
#long_description='Convert text from a file or from stdin into SQL table and query it instantly. Uses sqlite as backend. The idea is to make SQL into a tool on the command line or in scripts.'

setup(name='termsql',
      version='1.0',
      description='Convert text from a file or from stdin into SQL table and query it instantly. Uses sqlite as backend. The idea is to make SQL into a tool on the command line or in scripts.',
      long_description=long_description,
      author='Tobias Glaesser',
      author_email='tobimensch@gmail.com',
      url='https://github.com/tobimensch/termsql',
      scripts=['termsql','where','limit','groupby','orderby','select'],
      data_files=[('/usr/share/man/man1/', ['termsql.1.gz'])],
      install_requires=['sqlparse'],
      license='MIT'
     )


