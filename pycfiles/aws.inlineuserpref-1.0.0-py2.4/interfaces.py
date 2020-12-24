# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/aws/inlineuserpref/interfaces.py
# Compiled at: 2009-12-13 18:44:30
"""aws.inlineuserpref public interfaces"""
from zope.interface import Interface

class IAWSInlineUserPrefLayer(Interface):
    """Our local layer that marks installation"""
    __module__ = __name__