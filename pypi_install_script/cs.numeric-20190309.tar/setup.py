#!/usr/bin/env python
from setuptools import setup
setup(
  name = 'cs.numeric',
  description = 'some numeric functions; currently primes() and factors()',
  author = 'Cameron Simpson',
  author_email = 'cs@cskk.id.au',
  version = '20190309',
  url = 'https://bitbucket.org/cameron_simpson/css/commits/all',
  classifiers = ['Development Status :: 6 - Mature', 'Programming Language :: Python', 'Programming Language :: Python :: 2', 'Programming Language :: Python :: 3', 'Intended Audience :: Developers', 'Operating System :: OS Independent', 'Topic :: Software Development :: Libraries :: Python Modules', 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'],
  include_package_data = True,
  install_requires = [],
  keywords = ['python2', 'python3'],
  license = 'GNU General Public License v3 (GPLv3)',
  long_description = 'A few ad hoc numeric alogrithms: `factors` and `primes`.\n\n## Function `factors(n)`\n\nGenerator yielding the prime factors of `n` in order from lowest to highest.\n\n## Function `primes()`\n\nGenerator yielding the primes in order starting at 2.',
  long_description_content_type = 'text/markdown',
  package_dir = {'': 'lib/python'},
  py_modules = ['cs.numeric'],
)
