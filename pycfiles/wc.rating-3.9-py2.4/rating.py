# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/wc/rating/rating.py
# Compiled at: 2007-03-07 18:40:25
import zope.component, zope.interface, persistent.list
from zope.annotation import factory
from wc.rating.interfaces import IRating, IRatable

class Rating(persistent.Persistent):
    __module__ = __name__
    zope.interface.implements(IRating)
    zope.component.adapts(IRatable)

    def __init__(self):
        self.average = 0.0
        self.numberOfRatings = 0
        self.ratings = persistent.list.PersistentList()

    def rate(self, rating):
        ratings = self.ratings
        ratings.append(float(rating))
        self.numberOfRatings += 1
        self.average = sum(ratings) / len(ratings)


rating_adapter = factory(Rating)