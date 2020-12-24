#!/usr/bin/env python

"""Kegboard support library.

This package contains the Python protocol support for Kegboard.  For more
information on Kegboard, see http://kegbot.org/kegboard/
"""

DOCLINES = __doc__.split('\n')
SHORT_DESCRIPTION = DOCLINES[0]
LONG_DESCRIPTION = '\n'.join(DOCLINES[2:])
VERSION = '1.2.0'

from setuptools import setup, find_packages

setup(
  name='kegbot-kegboard',
  version=VERSION,
  description=SHORT_DESCRIPTION,
  long_description=LONG_DESCRIPTION,
  author='The Kegbot Project Contributors',
  author_email='info@kegbot.org',
  license='MIT',
  url='https://kegbot.org/',
  packages=find_packages(exclude=['testdata']),
  namespace_packages=['kegbot'],
  install_requires=['python-gflags', 'pyserial'],
  scripts = [
    'bin/kegboard-monitor.py',
    'bin/kegboard-tester.py',
    'bin/kegboard-info.py',
    'bin/set-kegboard-serialnumber',
  ],
)
