#!/usr/bin/python3

from setuptools import setup

setup(name='fhem-api',
      version='0.1.dev2',
      description='Python API for Fhem',
      author='Lukas Schulte',
      author_email='lukas@colorfreedom.org',
      url='https://colorfreedom.org/lukas/fhem-api',
      packages=['fhem'],
      install_requires=['requests'],
      )
