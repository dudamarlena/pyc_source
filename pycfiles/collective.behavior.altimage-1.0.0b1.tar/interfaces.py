# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/collective/beancounter/interfaces.py
# Compiled at: 2007-11-14 13:15:30
__author__ = 'Stefan Eletzhofer <stefan.eletzhofer@inquant.de>'
__docformat__ = 'plaintext'
__revision__ = '$Revision: 53835 $'
__version__ = '$Revision: 53835 $'[11:-2]
from zope import interface

class IBeanContable(interface.Interface):
    """ a content which is bean countable """
    __module__ = __name__


class IBeanCounter(interface.Interface):
    __module__ = __name__
    percentage = interface.Attribute('The percentage filled')


class IBeanCounterFieldFilter(interface.Interface):
    """ provide a filter method """
    __module__ = __name__

    def __call__(field):
        """ return true if the field is to be considered as
            countable """
        pass