# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ally/api/criteria.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on Jun 10, 2011\n\n@package: ally api\n@copyright: 2011 Sourcefabric o.p.s.\n@license: http://www.gnu.org/licenses/gpl-3.0.txt\n@author: Nistor Gabriel\n\nProvides general used criteria for APIs.\n'
from .type import Date, Time, DateTime
from ally.api.config import criteria

@criteria
class AsOrdered:
    """
    Provides query for properties that can be ordered.
    """
    ascending = bool
    priority = int

    def orderAsc(self):
        self.ascending = True

    def orderDesc(self):
        self.ascending = False


@criteria(main='like')
class AsLike:
    """
    Provides query for properties that can be managed by a like function, this will only handle string types
    """
    like = str
    ilike = str


@criteria
class AsLikeOrdered(AsLike, AsOrdered):
    """
    Provides the like search and also the ordering.
    """
    pass


@criteria(main='equal')
class AsEqual:
    """
    Provides query for properties that can be managed by a equal function, this will only handle string types.
    """
    equal = str


@criteria
class AsEqualOrdered(AsEqual, AsOrdered):
    """
    Provides the equal search and also the ordering.
    """
    pass


@criteria(main='value')
class AsBoolean:
    """
    Provides query for properties that can be managed as booleans.
    """
    value = bool


@criteria
class AsBooleanOrdered(AsBoolean, AsOrdered):
    """
    Provides the booleans search and also the ordering.
    """
    pass


@criteria(main=('start', 'end'))
class AsRange:
    """
    Provides a query for properties that need to be handled as a range.
    """
    start = str
    end = str
    since = str
    until = str


@criteria
class AsRangeOrdered(AsRange, AsOrdered):
    """
    Provides the equal search and also the ordering.
    """
    pass


@criteria(main=('start', 'end'))
class AsDate:
    """
    Provides query for properties that can be managed as date.
    """
    start = Date
    end = Date
    since = Date
    until = Date


@criteria
class AsDateOrdered(AsDate, AsOrdered):
    """
    Provides the date search and also the ordering.
    """
    pass


@criteria(main=('start', 'end'))
class AsTime:
    """
    Provides query for properties that can be managed as time.
    """
    start = Time
    end = Time
    since = Time
    until = Time


@criteria
class AsTimeOrdered(AsTime, AsOrdered):
    """
    Provides the time search and also the ordering.
    """
    pass


@criteria(main=('start', 'end'))
class AsDateTime:
    """
    Provides query for properties that can be managed as date time.
    """
    start = DateTime
    end = DateTime
    since = DateTime
    until = DateTime


@criteria
class AsDateTimeOrdered(AsDateTime, AsOrdered):
    """
    Provides the date time search and also the ordering.
    """
    pass