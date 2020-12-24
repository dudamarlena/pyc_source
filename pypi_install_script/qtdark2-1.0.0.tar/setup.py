#!/usr/bin/env python

import re
from setuptools import setup

_version = re.search(r'__version__\s+=\s+\'(.*)\'',
                     open('qtdark2/__init__.py').read()).group(1)

setup(name='qtdark2',
      version=_version,
      packages=['qtdark2'],
      description='Qt Widgets Modern User Interface',
      author='Breitburg Elias',
      author_email='contact@breitburg.me',
      url='https://www.github.com/upbits/qtdark2',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Software Development :: User Interfaces'
      ],
      package_data={
          'qtdark2': ['resources/*']
      },
      install_requires=['qtpy>=1.3.1'])
