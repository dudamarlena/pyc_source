#!/usr/bin/env python
# coding=utf-8
from setuptools import setup

setup(name='PyPake',
      version='1.1',
      description='Pythonic Make',
      author='MyFreeWeb',
      author_email='me@myfreeweb.ru',
      url='http://launchpad.net/pake',
      packages=['pakeapi'],
      scripts=['pypake'],
      install_requires=['pyyaml'],
      classifiers=[
          "Programming Language :: Python",
          "Operating System :: OS Independent",
          "Development Status :: 4 - Beta",
          "License :: OSI Approved :: Apache Software License",
          "Intended Audience :: Developers",
          "Topic :: Software Development",
          "Topic :: Software Development :: Build Tools",
          "Topic :: Software Development :: Libraries :: Python Modules",
      ],
)
