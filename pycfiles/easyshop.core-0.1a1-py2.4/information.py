# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/core/interfaces/information.py
# Compiled at: 2008-09-01 03:10:02
from zope.interface import Interface
from zope import schema
from easyshop.core.config import _

class IInformationContainer(Interface):
    """A container to hold information like terms and conditions.
    """
    __module__ = __name__


class IInformationPage(Interface):
    """A page to hold the information as HTML and downloadable file.
    """
    __module__ = __name__
    text = schema.Text(title=_('Text'), description=_('The information as HTML'), default='', required=False)
    text = schema.Bytes(title=_('File'), description=_('The information as downloadable file.'), required=False)


class IInformationManagement(Interface):
    """Provides methods to manage information pages.
    """
    __module__ = __name__

    def getInformationPage(id):
        """Returns information page by given id
        """
        pass

    def getInformationPages():
        """Returns all information pages.
        """
        pass

    def getInformationPagesFor(product):
        """Returns valid information pages for given product.
        """
        pass