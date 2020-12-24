# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/synthesis/setup.py
# Compiled at: 2011-01-23 16:19:11
from setuptools import setup, find_packages
import sys
version = '1.106'
install_requires = [
 'setuptools']
setup(name='synthesis', version=version, description='Health and Human Services Data Integration Server', license='MIT', author='Alexandria Consulting LLC', author_email='eric@alexandriaconsulting.com', url='http://xsd.alexandriaconsulting.com/repos/trunk/synthesis/src', packages=[
 'synthesis', 'synthesis.conf', 'synthesis.errcatalog'])
long_description = ('Health and Human Services Data Integration Server', )
classifiers = (
 [
  'License :: OSI Approved :: The MIT License',
  'Programming Language :: Python',
  'Intended Audience :: Human Services Practitioners',
  'Topic :: Human Services Data Integration'],)
keywords = ('human services data integration hmis 211 niem', )
license = ('MIT', )
install_requires = [
 'setuptools']