#!/usr/bin/env python

from os.path import exists

from setuptools import setup


setup(name='clones',
      version='0.0.1',
      description='placeholder for clones',
      url='http://github.com/lensacom/clones',
      maintainer='Krisztian Szucs',
      maintainer_email='szucs.krisztian@gmail.com',
      keywords='github clones',
      packages=['clones'],
      install_requires=[],  
      #extras_require=extras_require,
      tests_require=['pytest-mock', 'pytest'],
      zip_safe=False)
