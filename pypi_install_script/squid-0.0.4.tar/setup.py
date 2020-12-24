#!/usr/bin/env python3
from setuptools import setup

setup(name='squid',
      version='0.0.4',
      description='Dynamically distribute tasks in parallel.',
      author='Álvaro Abella',
      author_email='alvaroabascar@gmail.com',
      packages=['squid'],
      install_requires=['tqdm']
      )
