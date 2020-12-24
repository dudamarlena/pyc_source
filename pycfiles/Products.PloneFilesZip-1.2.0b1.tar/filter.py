# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\Products\PloneBooking\browser\filter.py
# Compiled at: 2008-11-19 15:28:58
__doc__ = '\n'
from Products.Five import BrowserView

class SelectOptions(BrowserView):
    """This class is used to render select options of booking filter :
    - type
    - category
    - resource"""
    __module__ = __name__

    def getTypeVocabulary(self, **filter_args):
        """Returns type vocabulary"""
        return ()

    def getCategoryVocabulary(self, **filter_args):
        """Returns category vocabulary"""
        return ()

    def getResourceVocabulary(self, **filter_args):
        """Returns resource vocabulary"""
        return ()