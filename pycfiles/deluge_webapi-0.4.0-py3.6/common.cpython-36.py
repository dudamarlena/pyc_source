# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/webapi/common.py
# Compiled at: 2018-09-28 07:59:15
# Size of source mod 2**32: 139 bytes
import pkg_resources, os

def get_resource(filename):
    return pkg_resources.resource_filename('webapi', os.path.join('data', filename))