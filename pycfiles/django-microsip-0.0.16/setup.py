# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Admin\Documents\GitHub\django-microsip\microsip\conf\app_template\setup.py
# Compiled at: 2014-11-11 15:35:16
import os
from setuptools import setup
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))
setup(name='{{ app_name }}', version='0.0.1', packages=[
 '{{ app_name }}'], include_package_data=True, license='BSD License', description='{{ app_name }}', long_description='README', url='', author='Servicios de Ingenieria Computacional', author_email='jesusmahererra@gmail.com', classifiers=[
 'Environment :: Web Environment',
 'Framework :: Django',
 'Intended Audience :: Developers',
 'License :: OSI Approved :: BSD License',
 'Operating System :: OS Independent',
 'Programming Language :: Python',
 'Programming Language :: Python :: 2.6',
 'Programming Language :: Python :: 2.7',
 'Topic :: Internet :: WWW/HTTP',
 'Topic :: Internet :: WWW/HTTP :: Dynamic Content'])