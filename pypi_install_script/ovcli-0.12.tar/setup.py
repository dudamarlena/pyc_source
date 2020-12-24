#!/usr/bin/env python3
from setuptools import setup

setup(name='ovcli',
      version='0.12',
      description='OpenvCloud command line client',
      author='Jo De Boeck',
      author_email='deboeck.jo@gmail.com',
      url='http://github.com/grimpy/ovcli',
      install_requires=['prompt-toolkit>=2.0', 'nose', 'nose-parameterized', 'requests', 'PyYAML>=5.1'],
      packages=['ovcli'],
      entry_points={'console_scripts': ['ovcli=ovcli.__main__:main', 'ovcsh=ovcli.shell:main']}
      )
