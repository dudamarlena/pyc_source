# -*- coding: utf-8 -*-

##############################################################################
# TTYLight-Python: easily stylize terminal text
##############################################################################
#
# Author: Travis Cardwell <travis.cardwell@yuzutechnology.com>
# Copyright: Copyright (c) 2013, Yuzu Technology, Inc.
#
# This file is subject to the terms and conditions defined in the License
# file included with this source code.
#
##############################################################################

"""\
TTYLight-Python is a Python (3.3 or higher) library and command-line utility
for easily stylizing terminal text.

The ``ttylight`` library encodes ANSI escape sequences to set text color and
intensity.  Use this library to easily stylize terminal text in your
application.

The ``ttylight.ttylog`` library is a logging library that stylizes terminal
logs and provides helpers for many common logging tasks.  For example, you can
easily add progress counters, timestamps, and *spinner*-style animations to
your application.

The ``ttylight`` command-line utility highlights string or regular expression
targets in streams of text.
"""

from setuptools import find_packages, setup

from ttylight import __version__ as version


setup(name='TTYLight-Python',
      version=version,
      author='Travis Cardwell',
      author_email='travis.cardwell@yuzutechnology.com',
      url='http://www.yuzutechnology.com/en/products/TTYLight-Python',
      description="easily stylize terminal text",
      long_description=__doc__,
      platforms=['POSIX'],
      classifiers=['Development Status :: 4 - Beta',
                   'Environment :: Console',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: MIT License',
                   'Operating System :: POSIX',
                   'Programming Language :: Python :: 3.3',
                   'Topic :: Software Development :: User Interfaces',
                   'Topic :: System :: Logging',
                   'Topic :: Terminals',
                   'Topic :: Text Processing :: Filters',
                   ],
      license='MIT License',
      packages=find_packages(exclude=['test', 'test.*']),
      entry_points={
          'console_scripts': [
              'ttylight = ttylight.cli:main'
          ]
      },
      )
