#!/usr/bin/env python
# License: Apache License 2.0
from setuptools import find_packages, setup


def readme():
    with open('README.md') as f:
        return f.read()


def requirements():
    with open('requirements.txt') as f:
        reqs = f.read().splitlines()
    return reqs


setup(name='halef-SETU',
      version='0.0.5',
      description=('halef-SETU provides an easy wrapper around SKLL models for '
                   'statistical language understanding as well as an easy to '
                   'API based on Flask'),
      long_description=readme(),
      keywords='halef SLU NLP',
      url='https://sourceforge.net/p/halef/halef-SETU',
      author='Patrick Lange, Rutuja Ubale',
      author_email='plange@ets.org, rubale@ets.org',
      license='Apache License 2.0',
      packages=find_packages(),
      include_package_data=True,
      install_requires=requirements(),
      zip_safe=False)
