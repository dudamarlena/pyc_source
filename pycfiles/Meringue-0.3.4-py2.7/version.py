# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/meringue/utils/version.py
# Compiled at: 2015-08-17 17:37:49
import logging
try:
    from verlib import NormalizedVersion
except ImportError:
    pass

def get_version(version):
    try:
        return str(NormalizedVersion.from_parts(*version))
    except NameError:
        logging.info('for better install verlib')
        return ('.').join([ str(j) for i in version for j in i ])