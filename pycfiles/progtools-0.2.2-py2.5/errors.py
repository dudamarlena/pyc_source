# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/progtools/errors.py
# Compiled at: 2009-10-15 11:10:23
"""Exception classes for progtools"""
__author__ = 'Ross Light'
__date__ = 'December 7, 2008'
__docformat__ = 'reStructuredText'
__license__ = 'MIT'
__all__ = ['UsageError']

class UsageError(Exception):
    """Exception that is raised when a program is used improperly."""
    pass