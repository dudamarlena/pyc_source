# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/c2/search/customdescription/browser/interfaces.py
# Compiled at: 2009-11-12 04:01:44
__doc__ = '\ninterfaces.py\n\nCreated by Manabu Terada on 2009-11-12.\nCopyright (c) 2009 CMScom. All rights reserved.\n'
from zope.interface import Interface

class ICustomPlone(Interface):
    __module__ = __name__

    def cropText(self, text, length, ellipsis='...'):
        """Crop text on a word boundary
        """
        pass