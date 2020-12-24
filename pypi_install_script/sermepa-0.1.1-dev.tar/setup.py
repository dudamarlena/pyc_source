#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Setup file for sermepa client.
"""

from distutils.core import setup

PACKAGES = ['sermepa', ]
PACKAGES_DATA = {'sermepa.tests': []}

setup(name='sermepa',
      description = """A client to submit payment orders to the Sermepa
      service.""",
      author='GISCE Enginyeria',
      author_email='devel@gisce.net',
      url='http://www.gisce.net',
      version='0.1.1-dev',
      license='General Public Licence 2',
      long_description='''Long description''',
      provides=['sermepa'],
      install_requires=[],
      packages=PACKAGES,
      package_data=PACKAGES_DATA,
      scripts=[],
      test_suite='sermepa.tests',
)
