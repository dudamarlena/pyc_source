# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/z3c/resourcecollector/utility.py
# Compiled at: 2008-07-29 15:59:13
import sha
from zope import interface
from zope import component
from interfaces import ICollectorUtility

class CollectorUtility(object):
    """utility"""
    interface.implements(ICollectorUtility)

    def __init__(self, content_type):
        self.resources = {}
        self.content_type = content_type

    def getUrl(self, context, request):
        h = {}
        h.update(request.response._headers)
        filetoreturn = self.getResources(request)
        request.response._headers = h
        x = sha.new()
        x.update(filetoreturn)
        return x.hexdigest()

    def getResources(self, request):
        filetoreturn = ''
        reducedrs = self.resources.values()
        orderedrs = sorted(reducedrs, cmp=lambda a, b: cmp(a['weight'], b['weight']))
        for resource in orderedrs:
            res = component.getAdapter(request, name=resource['resource'])
            res.__name__ = resource['resource']
            filetoreturn += res.GET() + '\n'

        return filetoreturn