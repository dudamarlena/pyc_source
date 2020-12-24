# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/anz/dashboard/browser/mergedrequestview.py
# Compiled at: 2010-09-26 21:53:54
import re, types, cjson
from Products.Five import BrowserView
from zope.interface import implements
from Acquisition import aq_base, aq_parent, aq_inner
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.utils import _checkPermission
from anz.dashboard import MSG_FACTORY as _
from anz.dashboard.interfaces import IMergedRequestView

class MergedRequestView(BrowserView):
    """ Return multi-categories data in one request to improve performance. """
    __module__ = __name__
    implements(IMergedRequestView)

    def getMergedData(self, requests=[], retJson=True):
        """ Execute multi-requests' in one request.
        
        @param requests
        a list contains requested view and method info, format like:
        [ 'requestId@@viewName/methodName?queryString',... ]
        
        note:
        queryString fit the valid http query string format:
        field1=value1&field2=value2&field3=value3...
        
        @param retJson
        format returned value to json format or not ( default True ) 
        
        @return a dict contains multi-requests' data or its json format
        {
        'request1': {
            'success': True,
            'msg': 'Get request1 information success.'
            'title': 'title',
            'description': 'desc',
            ...
            },
        'request2': {
            'success': True,
            'msg': 'Get request2 information success.'
            'tags': 'tag1,tag2,...',
            ...
            },
        }
        
        """
        context = self.context
        ret = {}
        pat = re.compile('([a-zA-Z_]\\w*)@@([a-zA-Z_]\\w*)/([a-zA-Z_]\\w*)\\??([a-zA-Z_].*)*')
        for r in requests:
            result = pat.match(r)
            if result:
                (id, viewName, methodName, queryStr) = result.groups()
                success = True
                msg = ''
                data = {}
                view = context.restrictedTraverse(viewName, None)
                if view is not None:
                    params = {}
                    if queryStr:
                        pairs = queryStr.split('&')
                        for p in pairs:
                            (k, v) = p.split('=')
                            if k.find(':') != -1:
                                k = k.split(':')[0]
                            params[k] = v

                    method = getattr(view, methodName, None)
                    if method and callable(method):
                        data = method(**params)
                    else:
                        success = False
                        msg = _('No method %s found.' % methodName)
                else:
                    success = False
                    msg = _('Fail to get view %s' % viewName)
                if not isinstance(data, types.DictType):
                    data = cjson.decode(data)
                ret[id] = {'success': success, 'msg': msg}
                ret[id].update(data)

        return retJson and cjson.encode(ret) or ret