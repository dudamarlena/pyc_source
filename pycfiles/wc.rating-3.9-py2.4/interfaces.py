# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/wc/rating/interfaces.py
# Compiled at: 2007-03-07 18:39:55
from zope.schema import Float, Int
from zope.interface import Interface
from zope.annotation.interfaces import IAnnotatable
from zope.i18nmessageid import MessageFactory
_ = MessageFactory('wc.rating')

class IRatable(IAnnotatable):
    """Marker interface that promises that an implementing object maybe
    rated using ``IRating`` annotations.
    """
    __module__ = __name__


class IRating(Interface):
    """Give and query rating about objects, such as recipes.
    """
    __module__ = __name__

    def rate(rating):
        """Rate the current object with `rating`.
        """
        pass

    average = Float(title=_('Average rating'), description=_('The average rating of the current object'), required=True)
    numberOfRatings = Int(title=_('Number of ratings'), description=_('The number of times the current has been rated'), required=True)