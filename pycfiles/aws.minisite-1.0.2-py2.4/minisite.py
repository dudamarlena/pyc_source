# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\aws\minisite\interfaces\minisite.py
# Compiled at: 2010-04-08 08:46:15
from zope import schema
from zope.interface import Interface
from zope.app.container.constraints import contains
from zope.app.container.constraints import containers
from aws.minisite import minisiteMessageFactory as _

class IMiniSite(Interface):
    """Minimal Site"""
    __module__ = __name__