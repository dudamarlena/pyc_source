# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/c2/search/customdescription/browser/interfaces.py
# Compiled at: 2009-11-12 04:01:44
"""
interfaces.py

Created by Manabu Terada on 2009-11-12.
Copyright (c) 2009 CMScom. All rights reserved.
"""
from zope.interface import Interface

class ICustomPlone(Interface):
    __module__ = __name__

    def cropText(self, text, length, ellipsis='...'):
        """Crop text on a word boundary
        """
        pass