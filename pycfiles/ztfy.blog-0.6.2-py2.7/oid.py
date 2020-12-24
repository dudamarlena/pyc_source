# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/blog/oid.py
# Compiled at: 2012-06-26 16:33:07
__docformat__ = 'restructuredtext'
from zope.intid.interfaces import IIntIds
from ztfy.blog.interfaces import IUniqueID, IBaseContent
from zope.component import adapts, getUtility
from zope.interface import implements

class UniqueIDAdapter(object):
    adapts(IBaseContent)
    implements(IUniqueID)

    def __init__(self, context):
        self.context = context

    @property
    def oid(self):
        intids = getUtility(IIntIds)
        return hex(intids.queryId(self.context))