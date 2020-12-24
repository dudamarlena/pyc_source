#!/usr/bin/env python
import os
import sys
from io import open
from setuptools import setup, find_packages


def readme():
    with open('README.md', encoding='utf-8') as f:
        return f.read()

setup(name='pymongoback',
      version='1.0.0',
      description='PyMongo Back is a simple Python library designed to help you create MongoDB Backups from both local and remote servers.',
      long_description=readme(),
      author='Rafa Munoz',
      author_email='rafa93m@gmail.com',
      url='https://github.com/RafaMunoz/PyMongoBack',
      packages=find_packages(),
      license='MIT',
      keywords='tools sysadmin backup mongodb mongodump',
      classifiers=[
          'Programming Language :: Python',
          'License :: OSI Approved :: MIT License',
          'Environment :: Console',
          'Topic :: Database',
          'Topic :: Software Development :: Build Tools',
          'Topic :: System :: Archiving :: Backup',
          'Intended Audience :: System Administrators'
      ]
      )
