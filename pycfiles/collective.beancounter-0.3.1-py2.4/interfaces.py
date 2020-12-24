# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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