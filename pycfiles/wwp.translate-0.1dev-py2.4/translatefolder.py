# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wwp/translate/interfaces/translatefolder.py
# Compiled at: 2009-08-11 10:03:27
from zope import schema
from zope.interface import Interface
from zope.app.container.constraints import contains
from zope.app.container.constraints import containers
from wwp.translate import translateMessageFactory as _

class Itranslatefolder(Interface):
    """language folder containing translator items"""
    __module__ = __name__