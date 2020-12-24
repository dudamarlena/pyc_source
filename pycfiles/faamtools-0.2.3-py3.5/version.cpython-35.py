# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/faamtools/version.py
# Compiled at: 2016-03-07 13:26:33
# Size of source mod 2**32: 2080 bytes
from os.path import join as pjoin
_version_major = 0
_version_minor = 2
_version_micro = 3
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
 'Operating System :: POSIX :: Linux',
 'Programming Language :: Python',
 'Topic :: Scientific/Engineering :: Atmospheric Science']
description = 'faamtools: a Python toolbox to read FAAM data'
long_description = '\n\nfaamtools\n========\nRead and process instrumental aircraft observations collected by\nUK\'s Facility for Airborne Atmospheric Measurements (FAAM)\n\n* core processed data\n* AVAPS dropsonde data\n* 2DS and CDP cloud probes\n\nLicense\n=======\n``faamtools`` is licensed under the terms of the MIT license. See the file\n"LICENSE" for information on the history of this software, terms & conditions\nfor usage, and a DISCLAIMER OF ALL WARRANTIES.\n\nAll trademarks referenced herein are property of their respective holders.\n\nCopyright (c) 2016--, Denis Sergeev, University of East Anglia \n'
NAME = 'faamtools'
MAINTAINER = 'Denis Sergeev'
MAINTAINER_EMAIL = 'dennis.sergeev@gmail.com'
DESCRIPTION = description
LONG_DESCRIPTION = long_description
URL = 'http://github.com/dennissergeev/faamtools'
DOWNLOAD_URL = ''
LICENSE = 'MIT'
AUTHOR = 'Denis Sergeev'
AUTHOR_EMAIL = 'dennis.sergeev@gmail.com'
MAJOR = _version_major
MINOR = _version_minor
MICRO = _version_micro
VERSION = __version__
PACKAGES = ['faamtools']