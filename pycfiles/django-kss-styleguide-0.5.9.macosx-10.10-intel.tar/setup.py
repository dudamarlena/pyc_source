# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tim/Projects/django_kss/VENV/lib/python2.7/site-packages/django_kss/setup.py
# Compiled at: 2014-11-20 06:43:14
import os
from setuptools import setup
BASE_DIR = os.path.dirname(__file__)
with open(os.path.join(BASE_DIR, 'README.rst')) as (readme):
    README = readme.read()
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))
setup(name='django-kss', version='0.1', packages=[
 'django_kss'], include_package_data=True, license='BSD License', description='A simple Django app to make styleguide', long_description=README, install_requires=[
 'pykss'], url='http://www.example.com/', author='Tim Hsu', author_email='tim.yellow@gmail.com', classifiers=[
 'Environment :: Web Environment',
 'Framework :: Django',
 'Intended Audience :: Developers',
 'License :: OSI Approved :: BSD License',
 'Operating System :: OS Independent',
 'Programming Language :: Python',
 'Topic :: Internet :: WWW/HTTP',
 'Topic :: Internet :: WWW/HTTP :: Dynamic Content'])