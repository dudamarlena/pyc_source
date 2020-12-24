# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/zif/headincludes/interfaces.py
# Compiled at: 2010-03-12 11:12:03
from zope.interface import Interface

class IHeadIncludeRegistration(Interface):
    """registration for including a url appropriately in the head of an
       html document"""

    def register(url):
        """register the url for inclusion"""
        pass