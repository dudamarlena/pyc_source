# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/python_project_starter/template/setup.py
# Compiled at: 2019-01-30 14:35:45
from setuptools import setup, find_packages
from os import path
with open(path.join(path.abspath(path.dirname(__file__)), 'README.md')) as (f):
    long_description = f.read()
setup(name='my_project', author='author', author_email='author_email', url='repository_url', version='1.0', description='description', long_description=long_description, packages=find_packages())