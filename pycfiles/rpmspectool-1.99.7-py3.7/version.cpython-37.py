# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/rpmspectool/version.py
# Compiled at: 2019-12-10 09:36:36
# Size of source mod 2**32: 153 bytes
import pkg_resources
try:
    version = pkg_resources.require('rpmspectool')[0].version
except pkg_resources.DistributionNotFound:
    version = 'git'