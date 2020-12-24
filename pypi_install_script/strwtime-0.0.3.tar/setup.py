#!/usr/bin/env python

from distutils.core import setup

setup(name='strwtime',
  version='0.0.3',
  description='Strwtime web service',
  author='Mikhail Efremov',
  author_email='meechanic.design@gmail.com',
  url='https://github.com/meechanic/strwtime',
  download_url = 'https://github.com/meechanic/strwtime/archive/v0_0_3.tar.gz',
  license="MIT",
  scripts=['bin/strwtime_runserver.py'],
  packages=['strwtime']
)
