# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/superdesk/media_archive/api/criteria.py
# Compiled at: 2013-10-02 09:54:57
"""
Created on Dec 13, 2012

@package: ally api
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Ioan-Vasile Pocol

Provides custom criteria for media archive multiplugin archive.
"""
from ally.api.config import criteria
from ally.api.criteria import AsOrdered
from ally.api.type import List

@criteria
class AsLikeExpression:
    """
    Provides query for properties that can be managed by a like function, this will only handle string types
    Also provides the boolean expression functionality, that in case of like string operator can had in the same all conditions

    inc - include - means that the value is mandatory for the given criteria
    ext - extend - means that the value is optional for the given criteria
    exc - exclude - means that the value if forbidden for the given criteria

    The query compose an 'and' condition with all 'inc' criteria, and all negated 'exc' criteria. Then it is made an or with all
    'ext' criteria
    """
    inc = List(str)
    ext = List(str)
    exc = List(str)


@criteria
class AsLikeExpressionOrdered(AsLikeExpression, AsOrdered):
    """
    Provides the like search and also the ordering and boolean expression functionality (see AsLikeExpression).
    """
    pass


@criteria(main='values')
class AsIn:
    """
    Provides query for properties that can be managed by 'IN' function applied to a list.
    """
    values = List(str)


@criteria(main='values')
class AsInOrdered(AsIn, AsOrdered):
    """
    Provides query for properties that can be managed by 'IN' function applied to a list.
    Also provides the ordering functionality.
    """
    pass