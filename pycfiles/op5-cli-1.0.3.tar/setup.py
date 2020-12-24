# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ozan/git_trees/op5-cli/op5lib/setup.py
# Compiled at: 2016-08-22 09:07:55
import inspect, os
os.chdir(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='op5lib', version='1.0a', author='Ozan Safi', author_email='ozansafi@gmail.com', py_modules=[
 'op5'], description="A python library for OP5's REST API", install_requires=[
 'requests>=2.3.0',
 'termcolor>=1.1.0'])