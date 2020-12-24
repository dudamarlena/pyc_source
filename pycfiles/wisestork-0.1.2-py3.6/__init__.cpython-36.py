# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wisestork/__init__.py
# Compiled at: 2019-06-13 09:35:55
# Size of source mod 2**32: 887 bytes
import pkg_resources

def version():
    package_metadata = pkg_resources.get_distribution('wisestork')
    return package_metadata.version