#!/usr/bin/env python

from setuptools import setup

setup(name='pyunifi',
      version='2.20.1',
      description='API for Ubiquity Networks UniFi controller',
      author='Caleb Dunn',
      author_email='finish.06@gmail.com',
      url='https://github.com/finish06/unifi-api',
      packages=['pyunifi'],
      scripts=['unifi-create-voucher', 'unifi-ls-clients'],
      classifiers=[],
      install_requires=['requests'],
      )
