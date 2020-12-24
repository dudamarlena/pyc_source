# -*- coding: utf-8 -*-
"""
Setup.py for gitInformation

Created on Tue Nov 24 10:57:24 2015

@author: Dominik
"""

from setuptools import setup

setup(
      name='gitInformation',
      version='1.0',
      description='This package allows you to print important information '
                  'about your local git repository.',
      url='https://github.com/dowa4213',
      author='Dominik Walther',
      author_email = 'dominik.wal@hotmail.de',
      license='MIT',
      keywords='IPython notebook GitHub ',
      py_modules=["gitInformation"],
      install_requires=['GitPython'],
      )
