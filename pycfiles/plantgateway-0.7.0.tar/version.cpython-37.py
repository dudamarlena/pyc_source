# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/plantflow/version.py
# Compiled at: 2020-01-24 14:51:48
# Size of source mod 2**32: 2014 bytes
from __future__ import absolute_import
import os.path as pjoin
_version_major = 0
_version_minor = 0
_version_micro = ''
_version_extra = ''
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
description = 'PlantFlow: for simulating and analyzing chemical and manufacturing plant data'
long_description = '\nPlantFlow\n=========\n\nLicense\n=======\n``plantflow`` is licensed under the terms of the MIT license. See the file\n"LICENSE" for information on the history of this software, terms & conditions\nfor usage, and a DISCLAIMER OF ALL WARRANTIES.\n\nAll trademarks referenced herein are property of their respective holders.\n\nCopyright (c) 2017--, Wesley Beckner, The University of Washington.\n'
NAME = 'plantflow'
MAINTAINER = 'Wesley Beckner'
MAINTAINER_EMAIL = 'wesleybeckner@gmail.com'
DESCRIPTION = description
LONG_DESCRIPTION = long_description
URL = 'http://github.com/wesleybeckner/plantflow'
DOWNLOAD_URL = ''
LICENSE = 'MIT'
AUTHOR = 'Wesley Beckner'
AUTHOR_EMAIL = 'wesleybeckner@gmail.com'
PLATFORMS = 'OS Independent'
MAJOR = _version_major
MINOR = _version_minor
MICRO = _version_micro
VERSION = __version__
PACKAGE_DATA = {'plantflow': [pjoin('data', '*')]}
REQUIRES = ['numpy']