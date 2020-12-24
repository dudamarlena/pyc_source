# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/iw/releaser/tests/data/my.package/setup.py
# Compiled at: 2008-04-29 08:14:19
"""
This module contains the tool of my.package
"""
import os
from setuptools import setup, find_packages
version = '0.1'
README = os.path.join(os.path.dirname(__file__), 'my', 'package', 'docs', 'README.txt')
long_description = open(README).read() + '\n\n'
setup(name='my.package', version=version, description='', long_description=long_description, classifiers=['Programming Language :: Python', 'Topic :: Software Development :: Libraries :: Python Modules'], keywords='', author='Ingeniweb', author_email='support@ingeniweb.com', url='', license='GPL', packages=find_packages(exclude=['ez_setup']), namespace_packages=['my'], include_package_data=True, zip_safe=False, install_requires=['setuptools', 'zope.testing'], entry_points='\n      # -*- Entry points: -*-\n      ')