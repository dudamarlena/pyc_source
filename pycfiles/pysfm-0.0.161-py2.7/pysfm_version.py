# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\pysfm\core\pysfm_version.py
# Compiled at: 2017-08-22 02:03:57
import pkg_resources

def get_version():
    version = pkg_resources.require('pysfm')[0].version
    return version