# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-intel/egg/tnefparse/__init__.py
# Compiled at: 2018-11-30 06:01:00
import warnings
from .tnef import TNEF, TNEFAttachment, TNEFObject

def parseFile(fileobj):
    """a convenience function that returns a TNEF object"""
    warnings.warn('parseFile will be deprecated after 1.3', DeprecationWarning)
    return TNEF(fileobj.read())