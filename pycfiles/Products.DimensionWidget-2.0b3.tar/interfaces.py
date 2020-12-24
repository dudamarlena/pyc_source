# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/Products/DigestoContentTypes/utilities/interfaces.py
# Compiled at: 2009-04-26 22:17:24
from zope.interface import Interface
from zope.app.container.constraints import contains
from zope import schema
from Products.DigestoContentTypes import DigestoContentTypesMessageFactory as _

class INormativaTypes(Interface):
    """Normativa Types.
    """
    __module__ = __name__
    types = schema.List(title=_('Normativa Types'), description=_('Normativa Types'), required=False, value_type=schema.TextLine(title='Type'))

    def get_types():
        """ Returns the types as a list of utf-8 encoded strings into ascii.
            Plone needs this kind of strings, while the input widget is managed
            with Zope 3 stuff like formlib, and it seems to prefer utf-8 strings
            instead. :S
        """
        pass