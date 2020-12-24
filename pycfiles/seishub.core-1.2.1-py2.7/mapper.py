# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\seishub\core\processor\resources\mapper.py
# Compiled at: 2010-12-23 17:42:43
"""
Mapper resources.
"""
from seishub.core.exceptions import NotAllowedError, SeisHubError
from seishub.core.processor.resources.resource import Resource
from twisted.web import http

class MapperResource(Resource):
    """
    Processor handler of a mapping resource.
    """

    def __init__(self, mapper, folderish=False, **kwargs):
        Resource.__init__(self, **kwargs)
        self.is_leaf = True
        self.mapper = mapper
        if hasattr(mapper, 'public'):
            self.public = True
        if folderish:
            self.folderish = True
            self.category = 'mapping-folder'
        else:
            self.folderish = False
            self.category = 'mapping'

    def getMetadata(self):
        if self.folderish:
            return {'permissions': 16877}
        else:
            return {'permissions': 33188}

    def render_GET(self, request):
        func = getattr(self.mapper, 'process_GET')
        if not func:
            msg = 'Method process_GET is not implemented.'
            raise NotImplementedError(msg)
        result = func(request)
        if isinstance(result, basestring):
            if isinstance(result, unicode):
                result = result.encode('utf-8')
            if not result:
                request.setHeader('content-type', 'text/plain; charset=UTF-8')
            return result
        if isinstance(result, dict):
            temp = {}
            for category, ids in result.items():
                if category in ('folder', ):
                    folderish = True
                else:
                    folderish = False
                for id in ids:
                    temp[id] = self._clone(folderish=folderish)

            return temp
        msg = 'A mapper must return a dictionary of categories and ids or ' + 'a basestring for a resulting document.'
        raise SeisHubError(msg, code=http.INTERNAL_SERVER_ERROR)

    def render_POST(self, request):
        func = getattr(self.mapper, 'process_POST', None)
        if not func:
            allowed_methods = getattr(self, 'allowedMethods', ())
            msg = 'This operation is not allowed on this resource.'
            raise NotAllowedError(allowed_methods=allowed_methods, message=msg)
        func(request)
        request.code = http.NO_CONTENT
        return ''

    def render_DELETE(self, request):
        func = getattr(self.mapper, 'process_DELETE', None)
        if not func:
            allowed_methods = getattr(self, 'allowedMethods', ())
            msg = 'This operation is not allowed on this resource.'
            raise NotAllowedError(allowed_methods=allowed_methods, message=msg)
        func(request)
        request.code = http.NO_CONTENT
        return ''

    def render_PUT(self, request):
        func = getattr(self.mapper, 'process_PUT', None)
        if not func:
            allowed_methods = getattr(self, 'allowedMethods', ())
            msg = 'This operation is not allowed on this resource.'
            raise NotAllowedError(allowed_methods=allowed_methods, message=msg)
        result = func(request)
        request.code = http.CREATED
        request.headers['Location'] = str(result)
        return ''

    def _clone(self, **kwargs):
        return self.__class__(self.mapper, **kwargs)