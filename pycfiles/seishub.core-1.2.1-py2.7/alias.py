# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\seishub\core\processor\resources\alias.py
# Compiled at: 2010-12-23 17:42:43
"""
Alias resources.
"""
from seishub.core.processor.resources.resource import Resource
from seishub.core.processor.resources.rest import RESTResource

class AliasResource(Resource):
    """
    Processor handler of a alias resource.
    """

    def __init__(self, expr, **kwargs):
        Resource.__init__(self, **kwargs)
        self.is_leaf = True
        self.folderish = True
        self.category = 'alias'
        self.expr = expr

    def getMetadata(self):
        return {'permissions': 16877}

    def render_GET(self, request):
        res_dict = request.env.catalog.query(self.expr, full=False)
        temp = {}
        for id in res_dict['ordered']:
            res = res_dict[id]
            temp[res['resource_name']] = RESTResource(res)

        return temp