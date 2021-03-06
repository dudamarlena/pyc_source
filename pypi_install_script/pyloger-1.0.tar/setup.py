##############################################################################
#
# Copyright (c) 2013 Web Consulting and Contributors.
# All Rights Reserved.
#
##############################################################################

import os
import sys

from setuptools import setup, find_packages

py_version = sys.version_info[:2]


if py_version < (2, 6):
    raise RuntimeError('On Python 2, Pyramid requires Python 2.6 or better')

here = os.path.abspath(os.path.dirname(__file__))
try:
    README = open(os.path.join(here, 'README.rst')).read()
    CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()
except IOError:
    README = CHANGES = ''

install_requires=[
    'setuptools',
    ]


setup(name='pyloger',
      version='1.0',
      description=('The descusr web application development framework, a '
                   'syslog project'),
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI",
        "License :: Repoze Public License",
        ],
      keywords='python syslog, pyloger',
      author="descusr",
      author_email="descusr@163.com",
      url="http://www.piadu.com",
      license="BSD-derived (http://www.repoze.org/LICENSE.txt)",
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires = install_requires
      )

