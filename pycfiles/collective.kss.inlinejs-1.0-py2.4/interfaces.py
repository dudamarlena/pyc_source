# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/collective/kss/inlinejs/interfaces.py
# Compiled at: 2009-05-29 04:39:14
from zope.interface import Interface

class IInlineJsCommands(Interface):
    """Inline js plugin for kss"""
    __module__ = __name__

    def execJs(selector, code, debug='0'):
        """You can pass a selector and the inline js code to be applied"""
        pass