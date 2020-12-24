# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\pysfm\core\pysfm_version.py
# Compiled at: 2017-08-22 02:03:57
import pkg_resources

def get_version():
    version = pkg_resources.require('pysfm')[0].version
    return version