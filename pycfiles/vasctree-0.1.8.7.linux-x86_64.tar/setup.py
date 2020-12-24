# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vasctrees/setup.py
# Compiled at: 2012-06-28 14:46:47
import ez_setup
ez_setup.use_setuptools()
from setuptools import setup, find_packages
setup(name='vasctree', version='0.1.5', description='Python Vascular Tree', author='Brian Chapman and Holly Berty', author_email='brchapman@ucsd.edu', packages=find_packages('src'), package_dir={'': 'src'}, install_requires=[
 'python>=2.6', 'numpy>=1.3', 'scipy>=0.7', 'networkx>=1.0.dev1492'])