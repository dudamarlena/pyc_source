# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/treeducken_tools/version.py
# Compiled at: 2019-09-09 15:49:26
# Size of source mod 2**32: 2938 bytes
from __future__ import absolute_import, division, print_function
import os.path as pjoin
_version_major = 0
_version_minor = 1
_version_micro = ''
_version_extra = 'dev'
_ver = [
 _version_major, _version_minor]
if _version_micro:
    _ver.append(_version_micro)
if _version_extra:
    _ver.append(_version_extra)
__version__ = '.'.join(map(str, _ver))
CLASSIFIERS = [
 'Development Status :: 3 - Alpha',
 'Environment :: Console',
 'Intended Audience :: Science/Research',
 'License :: OSI Approved :: MIT License',
 'Operating System :: OS Independent',
 'Programming Language :: Python',
 'Topic :: Scientific/Engineering']
description = 'treeducken_tools: a simulation study for testing sampling of DTL models'
long_description = '\ntreeducken_tools\n========\n\nThis study contains software implementations of simulation of species tree and gene trees under a duplication, transfer,\nand loss (DTL) model using the treeducken software (https://github.com/wadedismukes/treeducken), and the subsequent \nanalysis of these data. Specifically this study aims to address the effect of taxon sampling on these models with the \nintention of further characterize model performance. \n\nThe setup of ale-simulation-study is based on the Shablona template project for small scientific Python projects. \nSee more at http://github.com/uwescience/shablona. This templatecontains infrastructure for testing, documentation,\ncontinuous integration and deployment, which can be easily adapted\nto use in other projects.\n\nTo learn more about this project, please go to the\nrepository README_.\n.. _README: https://github.com/wadedismukes/dtl-simulation-study/master/README.md\nLicense\n=======\n``treeducken_tools`` is licensed under the terms of the MIT license. See the file\n"LICENSE" for information on the history of this software, terms & conditions\nfor usage, and a DISCLAIMER OF ALL WARRANTIES.\nAll trademarks referenced herein are property of their respective holders.\nCopyright (c) 2015--, Wade Dismukes, Iowa State University.\n'
NAME = 'treeducken_tools'
MAINTAINER = 'Wade Dismukes'
MAINTAINER_EMAIL = 'waded@iastate.edu'
DESCRIPTION = description
LONG_DESCRIPTION = long_description
URL = 'http://github.com/wadedismukes/dtl-simulation-study'
DOWNLOAD_URL = ''
LICENSE = 'MIT'
AUTHOR = 'Wade Dismukes'
AUTHOR_EMAIL = 'waded@iastate.edu'
PLATFORMS = 'OS Independent'
MAJOR = _version_major
MINOR = _version_minor
MICRO = _version_micro
VERSION = __version__
PACKAGE_DATA = {'treeducken_tools': [pjoin('data', '*')]}
REQUIRES = ['numpy']