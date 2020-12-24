# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wwp/shopfronts/interfaces/street_view.py
# Compiled at: 2009-09-22 12:28:00
from zope import schema
from zope.interface import Interface
from zope.app.container.constraints import contains
from zope.app.container.constraints import containers
from wwp.shopfronts import shopfrontsMessageFactory as _

class Istreet_view(Interface):
    """View a street of stores"""
    __module__ = __name__
    bodytext = schema.SourceText(title=_('Body Text for Street'), required=False, description=_('Enter the description of the street'))