# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/Plone-4.3.7-was-4.2.1/zeocluster/src/Products.ATSuccessStory/setup.py
# Compiled at: 2015-12-17 03:21:31
from setuptools import setup, find_packages
import os
version = '4.1.2'
setup(name='Products.ATSuccessStory', version=version, description='Success stories Product', long_description=open('README.txt').read() + '\n' + open(os.path.join('docs', 'HISTORY.txt')).read(), classifiers=[
 'Framework :: Plone',
 'Programming Language :: Python',
 'Topic :: Software Development :: Libraries :: Python Modules'], keywords='plone 3.1 atsuccessstory', author='Franco Pellegrini', author_email='frapell@menttes.com', url='http://plone.org/products/atsuccessstory', license='GPL', packages=find_packages(exclude=['ez_setup']), namespace_packages=[
 'Products'], include_package_data=True, zip_safe=False, install_requires=[
 'setuptools'], entry_points='\n      # -*- Entry points: -*-\n      ')