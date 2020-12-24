# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/base/index.py
# Compiled at: 2014-05-08 07:01:55
__docformat__ = 'restructuredtext'
from zopyx.txng3.core.interfaces import IIndexableContent
from ztfy.base.interfaces import IBaseContent
from zope.component import adapts
from zope.interface import implements
from zopyx.txng3.core.content import IndexContentCollector

class BaseContentTextIndexer(object):
    adapts(IBaseContent)
    implements(IIndexableContent)

    def __init__(self, context):
        self.context = context

    def indexableContent(self, fields):
        icc = IndexContentCollector()
        for field in fields:
            icc.addContent(field, getattr(self.context, field, None))

        return icc