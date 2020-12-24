# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\Products\PloneBooking\browser\filter.py
# Compiled at: 2008-11-19 15:28:58
"""
"""
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