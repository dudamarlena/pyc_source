# -*- coding: utf-8 -*-

from __future__ import with_statement

import sys
if sys.version_info < (3, 6):
    sys.exit('Python 3.6 or greater is required.')

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
    
import setuptools

import ziqiang


with open('README.md') as fp:
    readme = fp.read()

with open('LICENSE') as fp:
    license = fp.read()

setup(name = 'ziqiang',
      version = ziqiang.__version__,
      description = 'A package for reinforcement learning algorithms.',
      url='https://github.com/Li-Ming-Fan/ziqiang',
      #
      long_description = readme,
      long_description_content_type="text/markdown",
      author = 'Ming-Fan Li',
      author_email = 'li_m_f@163.com',
      maintainer='Ming-Fan Li',
      maintainer_email='li_m_f@163.com',      
      packages=setuptools.find_packages(),
      #license=license,
      platforms=['any'],
      classifiers=[]
      )
