#!/usr/bin/env python

from setuptools import find_packages, setup


setup(name='qwertyui',
      version='1.0.26',
      description='Some common Python functions and algorithms',
      author='Przemyslaw Kaminski',
      author_email='cgenie@gmail.com',
      url='https://github.com/CGenie/qwertyui',
      packages=find_packages(exclude=['tests.py']),
      install_requires=[
          'minio==4.0.3',
          'requests==2.20.0',
          'requests-toolbelt==0.8.0',
      ]
)
