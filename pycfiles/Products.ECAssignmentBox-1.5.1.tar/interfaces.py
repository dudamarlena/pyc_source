# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Products/eCards/interfaces.py
# Compiled at: 2008-11-11 20:26:20
from zope.interface import Interface

class IECard(Interface):
    """eCard interface
    """
    __module__ = __name__

    def thumbtag():
        """Generate image tag using the api of the ImageField
        """
        pass


class IECardCollection(Interface):
    """eCard Collection interface
    """
    __module__ = __name__


class IECardCollectionView(Interface):
    """eCard Collection browser view
    """
    __module__ = __name__

    def getCardsForView():
        """Return a two dimensional array of images representing
           the number of images intended per row.
        """
        pass


class IECardPopupView(Interface):
    """eCard Collection browser view
    """
    __module__ = __name__

    def stripNewLines(str):
        """This method strips out linefeeds from
           any string in an effort to clamp down
           on potential spam sending vulnerabilities.
        """
        pass

    def sendECard():
        """Calls send on the MailHost object, protected
           by our custom Send eCard permission
        """
        pass