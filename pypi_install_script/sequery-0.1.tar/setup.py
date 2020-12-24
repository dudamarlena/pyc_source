#!/usr/bin/env python

from setuptools import setup
from os.path import exists


setup(name='sequery',
      version='0.1',
      packages=['sequery'],
      description='sequery',
      url='http://github.com/kszucs/sequery',
      maintainer='Krisztian Szucs',
      maintainer_email='szucs.krisztian@gmail.com',
      license='BSD',
      keywords='',
      install_requires=[],
      tests_require=[],
      setup_requires=[],
      # long_description=(open('README.rst').read() if exists('README.rst')
      #                   else ''),
      zip_safe=False)
