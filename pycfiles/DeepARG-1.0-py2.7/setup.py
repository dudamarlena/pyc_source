# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/deeparg/setup.py
# Compiled at: 2019-10-26 23:30:30
from setuptools import setup, find_packages
setup(name='DeepARG', version='2.0', packages=find_packages(), include_package_data=True, install_requires=[
 'BioPython',
 'ete3',
 'h5py',
 'tqdm',
 'pandas',
 'networkx'], entry_points='\n        [console_scripts]\n        deeparg=GeneTools.entry:cli\n    ')