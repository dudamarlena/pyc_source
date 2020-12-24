# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/plone/oofill/interfaces.py
# Compiled at: 2008-04-03 08:53:09
__doc__ = '\n$Id$\n'
__author__ = 'Jean-Nicolas Bès <contact@atreal.net>'
__docformat__ = 'plaintext'
__licence__ = 'GPL'
from zope.interface import Attribute
from zope.interface import Interface

class IOOFillEngine(Interface):
    """
    """
    __module__ = __name__

    def fillInTheBlanks(odtfile, view):
        """
        Uses the view to fill the odtfile 'blanks'
        """
        pass