#!/usr/bin/python
from os.path import isfile
import codecs
import os
import re

from setuptools import setup


TOPDIR = os.path.dirname(__file__) or "."
with codecs.open(TOPDIR + "/google_finance/__init__.py", encoding='utf-8') as f:
    VERSION = re.search('__version__ = "([^"]+)"', f.read()).group(1)


setup(name="google-finance",
      version=VERSION,
      description="Google Finance API",
      author="Joao Daher Neto",
      author_email="joao.daher.neto@gmail.com",
      license="GNU General Public License 3",
      long_description="""
        The google-finance module provides extracting stock tickers information from Google Finance API.
      """,
      url='https://github.com/joaodaher/google-finance',
      packages=["google_finance",],
      requires=["requests", "dateutil"],
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.2',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Topic :: Software Development :: Libraries',
      ],
)
