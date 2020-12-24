# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/base/path.py
# Compiled at: 2014-05-08 10:20:31
__docformat__ = 'restructuredtext'
from ztfy.base.interfaces import IPathElements, IBaseContent
from zope.component import adapts
from zope.interface import implements
from zope.traversing.api import getPath

class PathElementsAdapter(object):
    adapts(IBaseContent)
    implements(IPathElements)

    def __init__(self, context):
        self.context = context

    @property
    def paths(self):
        result = []
        path = getPath(self.context)
        if not path.startswith('/'):
            return None
        else:
            elements = path.split('/')
            for index in range(len(elements)):
                result.append(('/').join(elements[0:index + 1]))

            return result[1:]