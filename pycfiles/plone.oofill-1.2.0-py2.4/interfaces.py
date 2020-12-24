# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/plone/oofill/interfaces.py
# Compiled at: 2008-04-03 08:53:09
"""
$Id$
"""
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