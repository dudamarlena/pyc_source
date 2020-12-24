#!/usr/bin/env python

from os.path import exists

from setuptools import setup


setup(name='apis',
      version='0.0.1',
      description='placeholder for APIs',
      url='http://github.com/lensacom/apis',
      maintainer='Krisztian Szucs',
      maintainer_email='szucs.krisztian@gmail.com',
      keywords='github libraries',
      packages=['apis'],
      install_requires=[],  
      #extras_require=extras_require,
      tests_require=['pytest-mock', 'pytest'],
      zip_safe=False)
