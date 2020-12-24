# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/h5pyd/version.py
# Compiled at: 2020-02-06 15:54:14
# Size of source mod 2**32: 1658 bytes
from __future__ import absolute_import
import distutils.version as _sv
import sys, numpy
version = '0.7.1'
hdf5_version = 'REST'
_exp = _sv(version)
version_tuple = _exp.version + ((
 ''.join((str(x) for x in _exp.prerelease)),) if _exp.prerelease is not None else ('', ))
api_version_tuple = (0, 7, 1)
api_version = '0.7.1'
__doc__ = 'This is h5pyd **%s**\n\n' % version
info = 'Summary of the h5py configuration\n---------------------------------\n\nh5pyd    %(h5pyd)s\nPython  %(python)s\nsys.platform    %(platform)s\nsys.maxsize     %(maxsize)s\nnumpy   %(numpy)s\n' % {'h5pyd':version,  'python':sys.version, 
 'platform':sys.platform, 
 'maxsize':sys.maxsize, 
 'numpy':numpy.__version__}