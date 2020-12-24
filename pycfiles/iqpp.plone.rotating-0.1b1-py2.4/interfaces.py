# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/iqpp/plone/rotating/interfaces.py
# Compiled at: 2008-08-04 05:41:36
from zope.interface import Interface
from zope import schema
from iqpp.plone.rotating.config import _

class IRotating(Interface):
    """Provides methods to get rotating items.
    """
    __module__ = __name__

    def getItem():
        """Returns next item.
        """
        pass

    def getItems():
        """Returns next items.
        """
        pass

    def setOptions(**kwargs):
        """Sets options.
        """
        pass


class IData(Interface):
    """Provides methods to get same kind of data from arbitrary objects.
    """
    __module__ = __name__

    def getContent(self):
        """Returns generic content of the item.
        """
        pass

    def getFooter():
        """Returns the footer of the item.
        """
        pass

    def getTitle():
        """Returns the title of the item.
        """
        pass

    def getURL():
        """Returns the URL of the item.
        """
        pass


class IRotatingOptions(Interface):
    """
    """
    __module__ = __name__
    show_already_selected = schema.Bool(title=_('Show Already Selected'), description=_('If checked, already selected items within "Path" can be displayed again. If unchecked all items within "Path" are displayed only once.'), required=False)
    reset_already_selected = schema.Bool(title=_('Reset Selected'), description=_('If checked already selected items within "Path" will be reset if all items has been displayed.'), required=False)
    update_intervall = schema.Int(title=_('Update Intervall'), description=_('Within this intervall the same object are returned.'), default=0, required=True)
    set_to_midnight = schema.Bool(title=_('Set To Midnight'), description=_('If checked "Last Update" is always set to midnight. This only makes sense if "Update Intervall" is set to an multiple of 24 hours.'), required=False)