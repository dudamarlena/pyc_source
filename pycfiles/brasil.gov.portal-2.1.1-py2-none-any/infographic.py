# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hvelarde/forcontent/idg/src/brasil.gov.portal/src/brasil/gov/portal/content/infographic.py
# Compiled at: 2018-10-18 17:35:13
from plone.dexterity.content import Item
from zope.interface import implementer
from zope.interface import Interface

class IInfographic(Interface):
    """Explicit marker interface for Infographic."""
    pass


@implementer(IInfographic)
class Infographic(Item):
    """Convinience subclass for Infographic portal type."""
    pass