#!/usr/bin/env python
# -*- coding:utf-8 -*-

import io

from setuptools import setup


version = '0.0.5'

def read(*parts):
    """Read file."""
    filename = os.path.join(os.path.abspath(os.path.dirname(__file__)), *parts)
    sys.stdout.write(filename)
    with io.open(filename, encoding="utf-8", mode="rt") as fp:
        return fp.read()


with open("README.md") as readme_file:
    readme = readme_file.read()

setup(name='python-mind',
      version=version,
      description='Python API for talking to MIND Mobility Connected Cars',
      long_description_content_type="text/markdown",
      long_description=readme,
      keywords='MIND Mobility PON Mijn Volkswagen Mijn Skoda Mijn Seat Audi Car Assistant Mijn Volkswagen Bedrijfswagens',
      author='Bram Kragten',
      author_email='mail@bramkragten.nl',
      url='https://github.com/bramkragten/python-mind/',
      packages=['mind'],
      install_requires=['requests>=2.0.0',
                        'requests_oauthlib>=0.7.0',
                        'oauthlib>=2.1.0']
      )
