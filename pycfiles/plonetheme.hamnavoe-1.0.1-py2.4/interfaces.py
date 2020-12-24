# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/plonetheme/hamnavoe/browser/interfaces.py
# Compiled at: 2008-09-27 12:33:26
from plone.theme.interfaces import IDefaultPloneLayer
from zope.interface import Interface

class IThemeSpecific(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 browser layer.
    """
    __module__ = __name__


class ISplashImage(Interface):
    """ Generates Hamnavoe splash image """
    __module__ = __name__

    def getSplashImage(self):
        """
          Get the splash image
        """
        pass


class IStrapline(Interface):
    """ Make the site strapline """
    __module__ = __name__

    def getStrapline(self):
        """
           Make the strapline
        """
        pass