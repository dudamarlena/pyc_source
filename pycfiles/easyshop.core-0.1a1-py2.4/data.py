# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/core/interfaces/data.py
# Compiled at: 2008-06-20 09:35:25
from zope.interface import Interface

class IData(Interface):
    """Provides methods to return content objects in several formats.
    """
    __module__ = __name__

    def asDict():
        """Returns context's attributes as dict.
        """
        pass