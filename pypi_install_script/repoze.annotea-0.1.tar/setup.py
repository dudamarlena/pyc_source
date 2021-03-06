##############################################################################
#
# Copyright (c) 2008 Agendaless Consulting and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the BSD-like license at
# http://www.repoze.org/LICENSE.txt.  A copy of the license should accompany
# this distribution.  THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL
# EXPRESS OR IMPLIED WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND
# FITNESS FOR A PARTICULAR PURPOSE
#
##############################################################################

__version__ = '0.1'

import os

from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

REQUIRES = ['rdflib < 3.0dev',
            'repoze.bfg',
            'repoze.bfg.restrequest',
            'repoze.catalog',
            'repoze.errorlog',
            'repoze.folder',
            'repoze.retry',
            'repoze.tm2',
            'repoze.zodbconn',
           ]

setup(name='repoze.annotea',
      version=__version__,
      description='Implement W3C Annotea server in repoze',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: WSGI",
        #"Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware",
        ],
      keywords='web wsgi zope annotation',
      author="Agendaless Consulting",
      author_email="repoze-dev@lists.repoze.org",
      url="http://www.repoze.org",
      license="BSD-derived (http://www.repoze.org/LICENSE.txt)",
      packages=find_packages(),
      include_package_data=True,
      namespace_packages=['repoze'],
      zip_safe=False,
      tests_require=[],
      install_requires=REQUIRES,
      test_suite="repoze.annotea",
      entry_points="""\
        [paste.app_factory]
        main = repoze.annotea.main:main
        [console_scripts]
        export_annotations = repoze.annotea.scripts.export_annotations:main
      """
      )

